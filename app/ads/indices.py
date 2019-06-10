"""Ad ES indices"""
from django_elasticsearch_dsl import DocType, Index, fields
from ads.models import Ad

ads_index = Index('ads')   # pylint: disable=C0103


@ads_index.doc_type
class AdDocument(DocType):
    """Ad document describing Index"""

    class Meta(object):
        """Metaclass config"""
        model = Ad

        fields = [
            'id',
            'title',
            'description',
            'updated_on',
            'created_on',
            'price',
            'name',
            'email',
            'phone',
        ]

    subcategory = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'name': fields.KeywordField(),
        'parent_category_name': fields.KeywordField(attr='parent_category.name'),
        'parent_category_id': fields.IntegerField(attr='parent_category.id'),
    })
