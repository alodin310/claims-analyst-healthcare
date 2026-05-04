with locations as (
    select distinct
        state,
        state_fips,
        city,
        zip_code,
        ruca_code,
        ruca_description,
        country
    from {{ ref('stg_cms_providers') }}
    where state is not null
)

select * from locations
