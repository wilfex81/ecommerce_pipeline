with source as (
    select * from {{ source('raw', 'order_payments') }}
),

renamed as (
    select
        order_id,
        payment_sequential          as payment_sequence,
        payment_type,
        payment_installments        as installments,
        payment_value               as amount
    from source
)

select * from renamed