with products as (
    select * from {{ ref('stg_products') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

product_stats as (
    select
        product_id,
        count(order_id)         as total_orders,
        sum(price)              as total_revenue,
        avg(price)              as avg_price,
        sum(freight)            as total_freight
    from order_items
    group by product_id
),

final as (
    select
        p.product_id,
        p.category,
        p.weight_grams,
        p.length_cm,
        p.height_cm,
        p.width_cm,
        p.photos_count,
        coalesce(ps.total_orders, 0)    as total_orders,
        coalesce(ps.total_revenue, 0)   as total_revenue,
        coalesce(ps.avg_price, 0)       as avg_price,
        coalesce(ps.total_freight, 0)   as total_freight
    from products p
    left join product_stats ps using (product_id)
)

select * from final