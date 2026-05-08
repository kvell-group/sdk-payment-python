from __future__ import annotations

from sdk_payment_python.models.payout import NominalPayout
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource


class NominalResource(BaseResource):
    def payout_by_requisites(
        self,
        transaction: str,
        amount: int,
        description: str,
        fio: str,
        inn: str,
        kvd: str,
        account_number: str,
        bank_bic: str,
        bank_cor_account: str,
        bank_name: str,
        snils: str | None = None,
        validate_self_employed: bool | None = None,
        customer: str | None = None,
        tax: dict | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
    ) -> NominalPayout:
        body: dict = {
            "transaction": transaction,
            "amount": amount,
            "description": description,
            "fio": fio,
            "inn": inn,
            "kvd": kvd,
            "account": {
                "account_number": account_number,
                "bank_bic": bank_bic,
                "bank_cor_account": bank_cor_account,
                "bank_name": bank_name,
            },
        }
        if snils is not None:
            body["snils"] = snils
        if validate_self_employed is not None:
            body["validate_self_employed"] = validate_self_employed
        if customer is not None:
            body["customer"] = customer
        if tax is not None:
            body["tax"] = tax
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        return NominalPayout.from_dict(
            self._post("/v1/orders/payout/smartcontract/fl/sber", body, self._rsa_headers(body))
        )

    def payout_sbp(
        self,
        transaction: str,
        amount: int,
        description: str,
        inn: str,
        kvd: str,
        phone: str,
        bank_bic: str,
        fio: str | None = None,
        fio_check: bool | None = None,
        validate_self_employed: bool | None = None,
        customer: str | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
    ) -> NominalPayout:
        body: dict = {
            "transaction": transaction,
            "amount": amount,
            "description": description,
            "inn": inn,
            "kvd": kvd,
            "phone": phone,
            "bank_bic": bank_bic,
        }
        if fio is not None:
            body["fio"] = fio
        if fio_check is not None:
            body["fio_check"] = fio_check
        if validate_self_employed is not None:
            body["validate_self_employed"] = validate_self_employed
        if customer is not None:
            body["customer"] = customer
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        return NominalPayout.from_dict(
            self._post("/v1/orders/payout/smartcontract/sbp/sber", body, self._rsa_headers(body))
        )


class AsyncNominalResource(AsyncBaseResource):
    async def payout_by_requisites(
        self,
        transaction: str,
        amount: int,
        description: str,
        fio: str,
        inn: str,
        kvd: str,
        account_number: str,
        bank_bic: str,
        bank_cor_account: str,
        bank_name: str,
        snils: str | None = None,
        validate_self_employed: bool | None = None,
        customer: str | None = None,
        tax: dict | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
    ) -> NominalPayout:
        body: dict = {
            "transaction": transaction,
            "amount": amount,
            "description": description,
            "fio": fio,
            "inn": inn,
            "kvd": kvd,
            "account": {
                "account_number": account_number,
                "bank_bic": bank_bic,
                "bank_cor_account": bank_cor_account,
                "bank_name": bank_name,
            },
        }
        if snils is not None:
            body["snils"] = snils
        if validate_self_employed is not None:
            body["validate_self_employed"] = validate_self_employed
        if customer is not None:
            body["customer"] = customer
        if tax is not None:
            body["tax"] = tax
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        return NominalPayout.from_dict(
            await self._post("/v1/orders/payout/smartcontract/fl/sber", body, self._rsa_headers(body))
        )

    async def payout_sbp(
        self,
        transaction: str,
        amount: int,
        description: str,
        inn: str,
        kvd: str,
        phone: str,
        bank_bic: str,
        fio: str | None = None,
        fio_check: bool | None = None,
        validate_self_employed: bool | None = None,
        customer: str | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
    ) -> NominalPayout:
        body: dict = {
            "transaction": transaction,
            "amount": amount,
            "description": description,
            "inn": inn,
            "kvd": kvd,
            "phone": phone,
            "bank_bic": bank_bic,
        }
        if fio is not None:
            body["fio"] = fio
        if fio_check is not None:
            body["fio_check"] = fio_check
        if validate_self_employed is not None:
            body["validate_self_employed"] = validate_self_employed
        if customer is not None:
            body["customer"] = customer
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        return NominalPayout.from_dict(
            await self._post("/v1/orders/payout/smartcontract/sbp/sber", body, self._rsa_headers(body))
        )