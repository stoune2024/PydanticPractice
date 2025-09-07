from files.task_3.shemas import (
    Deal,
    DealType,
    DatabaseConnection,
    DealsRepository,
)
from settings.settings import settings

deal_valid = Deal(
    id=123,
    title="title",
    comment="comment",
    created_at="2025-09-08",
    persons_in_charge=["steve", "bob"],
    deal_type=DealType.PURCHASE,
)


# deal_invalid = Deal(
#     id=123,
#     title="title",
#     comment=1234,
#     created_at="2025-09-08",
#     persons_in_charge=["steve", "bob"],
#     deal_type='smth',
# )


update_data = {"comment": "my_new_comment"}

with DatabaseConnection(settings.db_url) as conn:
    my_inst = DealsRepository(deal_models=[deal_valid], connection=conn)
    print(my_inst.deal_models)
    print(my_inst.update_deal(123, update_data))
