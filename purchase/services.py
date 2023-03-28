from django.db.models import Sum, QuerySet
from django.utils import timezone
from rest_framework.generics import get_object_or_404

from purchase.models import Order
from screening.models import Ticket
from users.models import User


class OrderingServiceError(Exception):
    pass


def get_user_cart(
    buyer: User,
    qs: QuerySet,
):
    added_to_cart_orders = (
        qs.filter(
            buyer=buyer,
            operation=Order.OrderOperation.ADD_TO_CART,
        )
        .select_related(
            "ticket",
        )
        .only(
            "ticket",
            "id",
        )
    )

    total_price = sum(
        Ticket.objects.filter(
            id__in=[i.ticket.id for i in added_to_cart_orders],
        )
        .annotate(total_price=Sum("price"))
        .values_list(
            "total_price",
            flat=True,
        )
    )

    return {
        "items": [
            {
                "id": i.id,
                "ticket": i.ticket.__dict__,
            }
            for i in added_to_cart_orders
        ],
        "total_price": total_price,
    }


def add_ticket_to_cart(
    buyer: User,
    ticket: Ticket,
) -> Order:
    operation = Order.OrderOperation.ADD_TO_CART

    if ticket.is_sold:
        raise OrderingServiceError(
            "Ticket can't be added to cart, it's already sold",
        )

    if timezone.now() > ticket.session_date_time:
        raise OrderingServiceError(
            "Screening session in past",
        )

    return Order.objects.create(
        buyer=buyer,
        ticket=ticket,
        operation=operation,
    )


def remove_ticket_from_cart(
    buyer: User,
    order_id: int,
):
    Order.objects.filter(
        id=order_id,
        buyer=buyer,
        operation=Order.OrderOperation.ADD_TO_CART,
    ).delete()


def buy_ticket(
    order_id: int,
    user: User,
):
    order = get_object_or_404(
        Order.objects.select_related(
            "ticket",
        ),
        pk=order_id,
    )

    if order.ticket.price > user.balance:
        raise OrderingServiceError(
            "insufficient funds",
        )

    if timezone.now() > order.ticket.session_date_time:
        raise OrderingServiceError("Screening session in past")

    order.operation = order.OrderOperation.PURCHASE
    order.ticket.is_sold = True
    user.balance = user.balance - order.ticket.price
    order.ticket.save()
    order.save()
    user.save()
