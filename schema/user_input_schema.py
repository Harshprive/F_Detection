from pydantic import BaseModel , Field , computed_field , model_validator
# -----------------------------
# Request schema
# -----------------------------
class Transaction(BaseModel):
    account_age_days: int = Field(..., ge=0, le=5000, description="Days since account creation")
    total_transactions: int = Field(..., ge=0, le=100000, description="Total completed transactions")
    failed_payments: int = Field(..., ge=0, le=1000, description="Failed payment attempts")
    transaction_amount: float = Field(..., gt=0, le=500000, description="Current transaction amount")
    transaction_hour: int = Field(..., ge=0, le=23, description="Hour of day (0–23)")
    is_vpn: int = Field(..., ge=0, le=1, description="1 if VPN detected, else 0")
    txn_count_last_1h: int = Field(..., ge=0, le=500, description="Transactions in last hour")
    location_mismatch: int = Field(..., ge=0, le=1, description="1 if geo mismatch detected")
    avg_amount_last_30d: float = Field(..., ge=0, le=500000, description="Average transaction amount (30 days)")


    @model_validator(mode="after")
    def logical_checks(self):
        if self.failed_payments > self.total_transactions:
            raise ValueError("failed_payments cannot exceed total_transactions")
        return self