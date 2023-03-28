import pytest
from rest_framework import status
from django.test.client import Client

from purchase.models import Order
from purchase.services import OrderingServiceError
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
    ):
        ticket, other_ticket = screening_session_with_tickets.tickets.values_list(
            "id",
            "price",
            "is_sold",
            "session_date_time",
            named=True,
        )[:2]

        api_test_client.post(
            self.api_cart_endpoint,
            data={
                "ticket": ticket.id,
            },
        )
        api_test_client.post(
            self.api_cart_endpoint,
            data={
                "ticket": other_ticket.id,
            },
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
    ):
        ticket_to_add = screening_session_with_tickets.tickets.first()
        api_test_client.post(
            self.api_cart_endpoint,
            data={
                "ticket": ticket_to_add.id,
            },
        )
        response = api_test_client.get(
            self.api_cart_endpoint,
        )
        order_id = response.json()["items"][0]["id"]
        response = api_test_client.delete(
            self.api_endpoint + f"{order_id}/delete_from_cart/"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = api_test_client.get(
            self.api_cart_endpoint,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"items": [], "total_price": 0.0}

    def test_buy_ticket(
        self,
        test_superuser: User,
        api_test_client: Client,
        screening_session_with_tickets: ScreeningSession,
    ):
        origin_user_balance = test_superuser.balance
        ticket_to_buy = screening_session_with_tickets.tickets.first()
        api_test_client.post(
            self.api_cart_endpoint,
            data={
                "ticket": ticket_to_buy.id,
            },
        )
        cart_response = api_test_client.get(
            self.api_cart_endpoint,
        )
        order_id = cart_response.json()["items"][0]["id"]

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
        api_test_client.post(
            self.api_cart_endpoint,
            data={
                "ticket": ticket_to_buy.id,
            },
        )
        cart_response = api_test_client.get(
            self.api_cart_endpoint,
        )
        order_id = cart_response.json()["items"][0]["id"]

        with pytest.raises(OrderingServiceError):
            api_test_client.post(
                self.api_endpoint + f"{order_id}/buy_ticket/",
            )
