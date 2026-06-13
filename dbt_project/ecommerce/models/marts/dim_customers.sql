with customers as(
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),


customer_orders as (
    select 
        customer_unique_id,
        count(o.order_id)           as total_orders,
        min(o.purchased_at)         as first_order_at,
        max(o.purchased_at)         as last_order_at
    from customers c
    left join orders o using (customer_id)
    group by customer_unique_id
), 

final as (
    select 
        c.customer_id,
        c.customer_unique_id,
        c.city,
        c.state,
        c.zip_code,
        co.total_orders,
        co.first_order_at,
        co.last_order_at

    from customers c
    left join customer_orders co using (customer_unique_id)
)

select * from final