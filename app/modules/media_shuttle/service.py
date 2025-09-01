# Business logic for Media Shuttle transfers
from typing import List
from . import schemas

# In-memory database for demonstration
fake_db = {
    1: schemas.Transfer(id=1, source_path="/mnt/source/file1.mov", destination_path="/mnt/dest/file1.mov", status="completed"),
    2: schemas.Transfer(id=2, source_path="/mnt/source/file2.exr", destination_path="/mnt/dest/file2.exr", status="pending"),
}

class MediaShuttleService:
    def get_all_transfers(self) -> List[schemas.Transfer]:
        return list(fake_db.values())

    def get_transfer_by_id(self, transfer_id: int) -> schemas.Transfer | None:
        return fake_db.get(transfer_id)

    def create_transfer(self, transfer: schemas.TransferCreate) -> schemas.Transfer:
        new_id = max(fake_db.keys()) + 1 if fake_db else 1
        new_transfer = schemas.Transfer(id=new_id, **transfer.model_dump())
        fake_db[new_id] = new_transfer
        return new_transfer

    def update_transfer(self, transfer_id: int, transfer_update: schemas.TransferUpdate) -> schemas.Transfer | None:
        if transfer_id not in fake_db:
            return None
        stored_transfer = fake_db[transfer_id]
        update_data = transfer_update.model_dump(exclude_unset=True)
        updated_transfer = stored_transfer.model_copy(update=update_data)
        fake_db[transfer_id] = updated_transfer
        return updated_transfer

    def delete_transfer(self, transfer_id: int) -> schemas.Transfer | None:
        if transfer_id not in fake_db:
            return None
        return fake_db.pop(transfer_id)

media_shuttle_service = MediaShuttleService()
