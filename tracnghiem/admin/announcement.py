import peewee
from playhouse.shortcuts import model_to_dict

from tracnghiem.admin.data_list import DataList
from tracnghiem.database import Announcement
from tracnghiem.utils.datetime import local_dt_from_timestamp

AnnouncementList = DataList("announcement")

AnnouncementList.set_template("admin_announcement.html")


@AnnouncementList.get_func
def announcement_get():
    query = Announcement.select().order_by(-Announcement.time)
    return [{
                "id"   : entry.id,
                "value": model_to_dict(entry, exclude = [Announcement.id])
            } for entry in query]


@AnnouncementList.add_func
def announcement_add(value):
    if 'title' not in value or 'content' not in value or 'time' not in value:
        return None
    try:
        time = local_dt_from_timestamp(int(value['time']))
    except ValueError:
        return None
    try:
        entry = Announcement.create(title = value['title'], content = value['content'], time = time)
        return entry.id
    except peewee.PeeweeException:
        return None


@AnnouncementList.remove_func
def announcement_remove(id: int):
    try:
        entry = Announcement.get(id = id)
    except Announcement.DoesNotExist:
        return False
    entry.delete_instance()
    return True
