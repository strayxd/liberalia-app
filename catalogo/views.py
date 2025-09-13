# catalogo/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import LibroFicha

@login_required
def libro_detalle(request, isbn):
    # Normaliza ISBN (acepta con o sin guiones/espacios)
    isbn_norm = isbn.replace("-", "").replace(" ", "").strip()

    obj = get_object_or_404(
        LibroFicha.objects.select_related("editorial").filter(
            Q(isbn=isbn) | Q(isbn=isbn_norm) | Q(isbn__iexact=isbn)
        )
    )
    return render(request, "catalogo/libro_detalle.html", {"obj": obj})

