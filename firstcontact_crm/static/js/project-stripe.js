var style = {
  base: {
    color: "#32325d",
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4"
    }
  },
  invalid: {
    color: "#fa755a",
    iconColor: "#fa755a"
  }
};

console.log("In Checkout JS ====")

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let priceId = "{{ pricing_tier.stripe_price_id }}"
let stripe = Stripe("{{ STRIPE_PUBLIC_KEY }}");
let elements = stripe.elements();
let card = elements.create('card', { style: style });

card.mount('#card-element');
card.on('change', function (event) {
  displayError(event);
});

function displayError(event) {
  //changeLoadingState(false);
  let displayError = document.getElementById('card-element-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
}

const form = document.querySelector('#payment-form');
form.addEventListener('submit', async (e) => {
  // Don't fully submit the form.
  e.preventDefault();

  changeLoadingState(true);
  setMessage("Subscribing... please wait.");

  // Tokenize the payment method.
  //
  // This makes a client side API call to Stripe to pass the payment
  // details and returns either an error or a new paymentMethod object that
  // we'll pass when creating the Subscription.
  const nameInput = document.querySelector('#name');

  // If a previous payment was attempted, get the latest invoice
  const latestInvoicePaymentIntentStatus = localStorage.getItem(
      'latestInvoicePaymentIntentStatus'
  );
  if (latestInvoicePaymentIntentStatus === 'requires_payment_method') {
    const invoiceId = localStorage.getItem('latestInvoiceId');
    const isPaymentRetry = true;
    // create new payment method & retry payment on invoice with new payment method
    createPaymentMethod({
      card,
      isPaymentRetry,
      invoiceId,
    });
  } else {
    // create new payment method & create subscription
    createPaymentMethod({ card });
  } 
});

function createPaymentMethod({ card, isPaymentRetry, invoiceId }) {
const customerId = "{{ request.user.stripe_customer_id }}";
// Set up payment method for recurring usage
let billingName = document.querySelector('#name').value;

let priceId = "{{ pricing_tier.stripe_price_id }}"

stripe
  .createPaymentMethod({
    type: 'card',
    card: card,
    billing_details: {
      name: billingName,
    },
  })
  .then((result) => {
    if (result.error) {
      changeLoadingState(false);
      displayError(result);
    } else {
      if (isPaymentRetry) {
        // Update the payment method and retry invoice payment
        retryInvoiceWithNewPaymentMethod({
          paymentMethodId: result.paymentMethod.id,
          invoiceId: invoiceId,
          priceId: priceId,
        });
      } else {
      createSubscription({
        customerId: customerId,
        paymentMethodId: result.paymentMethod.id,
        priceId: priceId,
      });
      }
    }
  });
}

function createSubscription({ customerId, paymentMethodId, priceId }) {
return (
  fetch("{% url 'payment:create-subscription' %}", {
    method: 'post',
    headers: {
      'Content-type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      customerId: customerId,
      paymentMethodId: paymentMethodId,
      priceId: priceId,
    }),
  })
    .then((response) => {
      return response.json();
    })
    // If the card is declined, display an error to the user.
    .then((result) => {
      if (result.error) {
        // The card had an error when trying to attach it to a customer.
        throw result;
      }
      return result;
    })
    // Normalize the result to contain the object returned by Stripe.
    // Add the additional details we need.
    .then((result) => {
      return {
        paymentMethodId: paymentMethodId,
        priceId: priceId,
        subscription: result,
      };
    })
    // Some payment methods require a customer to be on session
    // to complete the payment process. Check the status of the
    // payment intent to handle these actions.
    .then(handlePaymentThatRequiresCustomerAction)
    // If attaching this card to a Customer object succeeds,
    // but attempts to charge the customer fail, you
    // get a requires_payment_method error.
    .then(handleRequiresPaymentMethod)
    // No more actions required. Provision your service for the user.
    .then(onSubscriptionComplete)
    .catch((error) => {
      // An error has happened. Display the failure to the user here.
      // We utilize the HTML element we created.
      changeLoadingState(false);
      displayError(error);
    })
);
}

function retryInvoiceWithNewPaymentMethod({
customerId,
paymentMethodId,
invoiceId,
priceId
}) {
return (
  fetch("{% url 'payment:retry-invoice' %}", {
    method: 'post',
    headers: {
      'Content-type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      customerId: customerId,
      paymentMethodId: paymentMethodId,
      invoiceId: invoiceId,
    }),
  })
    .then((response) => {
      return response.json();
    })
    // If the card is declined, display an error to the user.
    .then((result) => {
      if (result.error) {
        // The card had an error when trying to attach it to a customer.
        throw result;
      }
      return result;
    })
    // Normalize the result to contain the object returned by Stripe.
    // Add the additional details we need.
    .then((result) => {
      return {
        // Use the Stripe 'object' property on the
        // returned result to understand what object is returned.
        invoice: result,
        paymentMethodId: paymentMethodId,
        priceId: priceId,
        isRetry: true,
      };
    })
    // Some payment methods require a customer to be on session
    // to complete the payment process. Check the status of the
    // payment intent to handle these actions.
    .then(handlePaymentThatRequiresCustomerAction)
    // No more actions required. Provision your service for the user.
    .then(onSubscriptionComplete)
    .catch((error) => {
      // An error has happened. Display the failure to the user here.
      // We utilize the HTML element we created.
      changeLoadingState(false);
      displayError(error);
    })
);
}

function cancelSubscription() {
return fetch("{% url 'payment:cancel-subscription' %}", {
  method: 'post',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken
  },
  body: JSON.stringify({
    subscriptionId: subscriptionId,
  }),
})
  .then(response => {
    return response.json();
  })
  .then(cancelSubscriptionResponse => {
    // Display to the user that the subscription has been cancelled.
  });
}

function updateSubscription(priceId, subscriptionId) {
return fetch("{% url 'payment:change-subscription' %}", {
  method: 'post',
  headers: {
    'Content-type': 'application/json',
    'X-CSRFToken': csrftoken
  },
  body: JSON.stringify({
    subscriptionId: subscriptionId,
    newPriceId: priceId,
  }),
})
  .then(response => {
    return response.json();
  })
  .then(response => {
    return response;
  });
}

function retrieveUpcomingInvoice(
customerId,
subscriptionId,
newPriceId,
trialEndDate
) {
return fetch("{% url 'payment:retrieve-upcoming-invoice' %}", {
  method: 'post',
  headers: {
    'Content-type': 'application/json',
    'X-CSRFToken': csrftoken
  },
  body: JSON.stringify({
    customerId: customerId,
    subscriptionId: subscriptionId,
    newPriceId: newPriceId,
  }),
})
  .then(response => {
    return response.json();
  })
  .then(response => {
    return response;
  });
}

function retrieveCustomerPaymentMethod(paymentMethodId) {
return fetch("{% url 'payment:retrieve-customer-payment-method' %}", {
  method: 'post',
  headers: {
    'Content-type': 'application/json',
    'X-CSRFToken': csrftoken
  },
  body: JSON.stringify({
    paymentMethodId: paymentMethodId,
  }),
})
  .then((response) => {
    return response.json();
  })
  .then((response) => {
    return response;
  });
}

function handlePaymentThatRequiresCustomerAction({
subscription,
invoice,
priceId,
paymentMethodId,
isRetry,
}) {
if (subscription && subscription.status === 'active') {
  // Subscription is active, no customer actions required.
  return { subscription, priceId, paymentMethodId };
}

// If it's a first payment attempt, the payment intent is on the subscription latest invoice.
// If it's a retry, the payment intent will be on the invoice itself.
let paymentIntent = invoice ? invoice.payment_intent : subscription.latest_invoice.payment_intent;

if (
  paymentIntent.status === 'requires_action' ||
  (isRetry === true && paymentIntent.status === 'requires_payment_method')
) {
  return stripe
    .confirmCardPayment(paymentIntent.client_secret, {
      payment_method: paymentMethodId,
    })
    .then((result) => {
      if (result.error) {
        // Start code flow to handle updating the payment details.
        // Display error message in your UI.
        // The card was declined (i.e. insufficient funds, card has expired, etc).
        throw result;
      } else {
        if (result.paymentIntent.status === 'succeeded') {
          // Show a success message to your customer.
          setMessage("Success! Redirecting to your account.");
          window.location.href = "{% url 'users:subscription' request.user.username %}"
        }
      }
    })
    .catch((error) => {
      changeLoadingState(false);
      displayError(error);
    });
} else {
  // No customer action needed.
  return { subscription, priceId, paymentMethodId };
}
}

function handleRequiresPaymentMethod({
subscription,
paymentMethodId,
priceId,
}) {
if (subscription.status === 'active') {
  // subscription is active, no customer actions required.
  return { subscription, priceId, paymentMethodId };
} else if (
  subscription.latest_invoice.payment_intent.status ===
  'requires_payment_method'
) {
  // Using localStorage to manage the state of the retry here,
  // feel free to replace with what you prefer.
  // Store the latest invoice ID and status.
  localStorage.setItem('latestInvoiceId', subscription.latest_invoice.id);
  localStorage.setItem(
    'latestInvoicePaymentIntentStatus',
    subscription.latest_invoice.payment_intent.status
  );
  throw { error: { message: 'Your card was declined.' } };
} else {
  return { subscription, priceId, paymentMethodId };
}
}

function onSubscriptionComplete(result) {
// Payment was successful.
if (result.subscription.status === 'active') {
    window.location.href = "{% url 'users:subscription' request.user.username %}"
  // Change your UI to show a success message to your customer.
  // Call your backend to grant access to your service based on
  // `result.subscription.items.data[0].price.product` the customer subscribed to.
}
}



function changeLoadingState(isLoading) {
if (isLoading) {
  document.querySelector('#button-text').classList.add('hidden');
  document.querySelector('#spinner').classList.remove('hidden');
  document.querySelector('#payment-form button').disabled = true;
} else {
  document.querySelector('#button-text').classList.remove('hidden');
  document.querySelector('#spinner').classList.add('hidden');
  document.querySelector('#payment-form button').disabled = false;
}
}


// helper method for displaying a status message.
const setMessage = (message) => {
const messageDiv = document.querySelector('#messages');
messageDiv.innerHTML += "<br>" + message;
} 