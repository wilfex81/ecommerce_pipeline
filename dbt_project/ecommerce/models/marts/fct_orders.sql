with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

payments as (
    select * from {{ ref('stg_order_payments') }}
),

reviews as (
    select * from {{ ref('stg_order_reviews') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

order_financials as (
    select
        order_id,
        sum(price)              as items_total,
        sum(freight)            as freight_total,
        sum(price + freight)    as order_total,
        count(*)                as item_count
    from order_items
    group by order_id
),

order_payments as (
    select
        order_id,
        sum(amount)             as amount_paid,
        count(distinct payment_type) as payment_methods
    from payments
    group by order_id
),

order_reviews as (
    select distinct on (order_id)
        order_id,
        score                   as review_score,
        created_at              as reviewed_at
    from reviews
    order by order_id, created_at desc
),

final as (
    select
        o.order_id,
        o.customer_id,
        c.customer_unique_id,
        c.city                          as customer_city,
        c.state                         as customer_state,
        o.status,
        o.purchased_at,
        o.approved_at,
        o.shipped_at,
        o.delivered_at,
        o.estimated_delivery_at,
        of.item_count,
        of.items_total,
        of.freight_total,
        of.order_total,
        op.amount_paid,
        op.payment_methods,
        r.review_score,
        r.reviewed_at,
        case
            when o.delivered_at <= o.estimated_delivery_at then true
            else false
        end                             as delivered_on_time
    from orders o
    left join customers c           using (customer_id)
    left join order_financials of   using (order_id)
    left join order_payments op     using (order_id)
    left join order_reviews r       using (order_id)
)

select * from final