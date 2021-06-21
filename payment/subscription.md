Subscription status changes =>
    Trailing --(expired) --> Free for life
    Trailing --(Upgrade) -->Basic,Essential, Enterprise

    Basic --(Cancelled ) --> Free for life   
    Basic --(Upgrade ) --> Essential, Enterprise

    Essential --(Cancelled ) --> Free for life   
    Essential --(Upgrade ) --> Basic, Enterprise

    Enterprise --(Cancelled ) --> Free for life   
    Enterprise --(Upgrade ) --> Basic, Essential

Internal subscription status - is active only when the subscription is active. else it is spaces.
1. Account create - Subscription - Training ( All features enabled for 7 days)
2. A batch job updates Subscription to Free for Life if Training period has ended and user has not selected any subscription (stauts is spaces)
3. User subscribes to pricing => Status is active 
4. User cancells the pricing plan =>  Status is spaces.