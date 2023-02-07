import uvicorn

from sqlalchemy import create_engine
from sqladmin import Admin
from settings import ProjectSettings
from fastapi import FastAPI
from api.router import event_router, account_router
from admin import InviteAdmin, EventInviteAdmin, EventAdmin, AccountAdmin

app = FastAPI()
app.include_router(account_router)
app.include_router(event_router)

admin = Admin(app, create_engine(ProjectSettings.sync_postgres_url))
admin.add_view(AccountAdmin)
admin.add_view(EventAdmin)
admin.add_view(EventInviteAdmin)
admin.add_view(InviteAdmin)


if __name__ == "__main__":
    uvicorn.run(app, host=ProjectSettings.host, port=ProjectSettings.port)
