import datetime
from unittest.mock import ANY

import pytest
from rest_framework import status
from django.test.client import Client

from purchase.models import Order
from purchase.services import (
    add_ticket_to_cart,
    buy_ticket,
    get_user_cart,
    return_purchased_ticket,
)
from screening.models import ScreeningSession
from users.models import User


@pytest.mark.django_db
class TestOrder:
    api_endpoint = "/api/order/"
    api_cart_endpoint = api_endpoint + "cart/"
    response_date_time_format = "%Y-%m-%dT%H:%M:%SZ"

    def test_add_ticket_to_cart(
        self,
        api_test_client: Client,
        screening_session_with_tickets: ScreeningSession,
    ):
        ticket_to_add = screening_session_with_tickets.tickets.first()
        response = api_test_client.post(
            self.api_cart_endpoint,
            data={
                "ticket": ticket_to_add.id,
            },
        )

        ticket_to_add.refresh_from_db()

        assert response.status_code == status.HTTP_201_CREATED
        assert ticket_to_add.orders.get().operation == Order.OrderOperation.ADD_TO_CART
        assert ticket_to_add.is_sold is False

    def test_get_cart(
        self,
        api_test_client: Client,
        screening_session_with_tickets: ScreeningSession,
        test_superuser: User,
    ):
        ticket, other_ticket = screening_session_with_tickets.tickets.all()[:2]

        add_ticket_to_cart(
            buyer=test_superuser,
            ticket=ticket,
        )
        add_ticket_to_cart(
            buyer=test_superuser,
            ticket=other_ticket,
        )

        response = api_test_client.get(
            self.api_cart_endpoint,
        )

        assert response.json() == {
            "items": [
                {
                    "id": 1,
                    "ticket": {
                        "id": ticket.id,
                        "price": str(ticket.price),
                        "is_sold": ticket.is_sold,
                        "session_date_time": ticket.session_date_time.strftime(
                            self.response_date_time_format,
                        ),
                    },
                },
                {
                    "id": 2,
                    "ticket": {
                        "id": other_ticket.id,
                        "price": str(other_ticket.price),
                        "is_sold": other_ticket.is_sold,
                        "session_date_time": other_ticket.session_date_time.strftime(
                            self.response_date_time_format,
                        ),
                    },
                },
            ],
            "total_price": ticket.price + other_ticket.price,
        }

    def test_remove_item_from_cart(
        self,
        api_test_client: Client,
        screening_session_with_tickets: ScreeningSession,
        test_superuser: User,
    ):
        ticket_to_add = screening_session_with_tickets.tickets.first()
        order_id = add_ticket_to_cart(
            buyer=test_superuser,
            ticket=ticket_to_add,
        ).id

        response = api_test_client.delete(
            self.api_endpoint + f"{order_id}/delete_from_cart/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert get_user_cart(
            buyer=test_superuser,
            qs=Order.objects.all(),
        ) == {"items": [], "total_price": 0.0}

    def test_buy_ticket(
        self,
        test_superuser: User,
        api_test_client: Client,
        screening_session_with_tickets: ScreeningSession,
    ):
        origin_user_balance = test_superuser.balance
        ticket_to_buy = screening_session_with_tickets.tickets.first()
        order_id = add_ticket_to_cart(
            buyer=test_superuser,
            ticket=ticket_to_buy,
        ).id

        response = api_test_client.post(
            self.api_endpoint + f"{order_id}/buy_ticket/",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        ticket_to_buy.refresh_from_db()
        test_superuser.refresh_from_db()

        assert (
            Order.objects.get(
                pk=order_id,
            ).operation
            == Order.OrderOperation.PURCHASE
        )
        assert ticket_to_buy.is_sold is True
        assert test_superuser.balance == origin_user_balance - ticket_to_buy.price

    def test_buy_ticket_error_not_enough_funds(
        self,
        test_superuser: User,
        api_test_client: Client,
        screening_session_with_tickets: ScreeningSession,
    ):
        test_superuser.balance = 1
        test_superuser.save()
        ticket_to_buy = screening_session_with_tickets.tickets.first()
        order_id = add_ticket_to_cart(
            buyer=test_superuser,
            ticket=ticket_to_buy,
        ).id

        response = api_test_client.post(
            self.api_endpoint + f"{order_id}/buy_ticket/",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "insufficient funds"}

    def test_return_ticket(
        self,
        api_test_client: Client,
        test_superuser: User,
        screening_session_with_tickets: ScreeningSession,
    ):
        origin_user_balance = test_superuser.balance
        ticket_to_return = screening_session_with_tickets.tickets.first()
        order_id = add_ticket_to_cart(
            buyer=test_superuser,
            ticket=ticket_to_return,
        ).id
        buy_ticket(
            order_id=order_id,
            buyer=test_superuser,
        )
        response = api_test_client.post(
            self.api_endpoint + f"{order_id}/return_ticket/",
        )

        test_superuser.refresh_from_db()
        ticket_to_return.refresh_from_db()
        screening_session_with_tickets.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert ticket_to_return.orders.filter(
            operation=Order.OrderOperation.RETURN
        ).exists()
        assert ticket_to_return.is_sold is False
        assert test_superuser.balance == origin_user_balance

    def test_return_ticket_fail_does_not_exists(
        self,
        api_test_client: Client,
    ):
        non_existing_order_id = 0
        response = api_test_client.post(
            self.api_endpoint + f"{non_existing_order_id}/return_ticket/",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_return_ticket_fail_session_already_started(
        self,
        api_test_client: Client,
        test_superuser: User,
        screening_session_with_tickets: ScreeningSession,
    ):
        ticket_to_return = screening_session_with_tickets.tickets.first()

        order_id = add_ticket_to_cart(
            buyer=test_superuser,
            ticket=ticket_to_return,
        ).id
        buy_ticket(
            order_id=order_id,
            buyer=test_superuser,
        )

        ticket_to_return.session_date_time -= datetime.timedelta(
            days=7,
        )
        ticket_to_return.save()

        response = api_test_client.post(
            self.api_endpoint + f"{order_id}/return_ticket/",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "detail": "Funds can't be returned. Screening session already started."
        }

    def test_return_ticket_fail_return_already_returned_ticket(
        self,
        api_test_client: Client,
        test_superuser: User,
        screening_session_with_tickets: ScreeningSession,
    ):
        ticket_to_return = screening_session_with_tickets.tickets.first()
        order_id = add_ticket_to_cart(
            buyer=test_superuser,
            ticket=ticket_to_return,
        ).id
        buy_ticket(
            order_id=order_id,
            buyer=test_superuser,
        )
        api_test_client.post(
            self.api_endpoint + f"{order_id}/return_ticket/",
        )
        response = api_test_client.post(
            self.api_endpoint + f"{order_id}/return_ticket/",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"detail": "Ticket is already returned"}

    def test_user_ordering_history(
        self,
        api_test_client: Client,
        test_superuser: User,
        screening_session_with_tickets: ScreeningSession,
    ):
        ticket = screening_session_with_tickets.tickets.first()

        add_order = add_ticket_to_cart(
            buyer=test_superuser,
            ticket=ticket,
        )
        buy_ticket(
            order_id=add_order.id,
            buyer=test_superuser,
        )
        return_order = return_purchased_ticket(
            buyer=test_superuser,
            order_id=add_order.id,
        )

        response = api_test_client.get(
            self.api_endpoint,
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "id": add_order.id,
                "operation": "PR",
                "date": ANY,
                "buyer": test_superuser.id,
                "ticket": 1,
            },
            {
                "id": return_order.id,
                "operation": "RT",
                "date": ANY,
                "buyer": test_superuser.id,
                "ticket": 1,
            },
        ]
