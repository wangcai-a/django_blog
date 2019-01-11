from data.models import ContentType, ReadNum
from django.db.models.fields import exceptions


class ReadNumExtend():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            re = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return re.read_num
        except exceptions.ObjectDoesNotExist:
            return 0