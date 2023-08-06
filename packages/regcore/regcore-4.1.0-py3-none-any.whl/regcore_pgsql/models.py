from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db import models

from regcore.models import Document


class DocumentIndex(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    combined_text = models.TextField()
    combined_titles = models.TextField()
    root_title = models.TextField()
    doc_root = models.SlugField(max_length=200)     # denormalized

    search_vector = SearchVectorField()

    @classmethod
    def from_document(cls, document):
        doc_and_children = document.get_descendants(include_self=True)
        return cls(
            document=document,
            combined_text='\n'.join(
                d.text for d in doc_and_children if d.text),
            combined_titles='\n'.join(
                d.title for d in doc_and_children if d.title),
            root_title=document.title or '',
            doc_root=document.label_string.split('-')[0],
        )

    @classmethod
    def rebuild_search_vectors(cls):
        cls.objects.update(search_vector=(
            # note that the root title gets double-counted, as it's also in
            # combined_titles
            SearchVector('root_title', weight='B') +
            SearchVector('combined_titles', weight='A') +
            SearchVector('combined_text', weight='B')
        ))
