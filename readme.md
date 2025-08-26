# 🏡 Estate Management (Módulo + Extensão Account)

Este projeto segue o tutorial oficial do Odoo (Capítulo 16 - Final Word).

---

## 📂 Estrutura

```
estate/
├── __init__.py
├── __manifest__.py
├── README.md
│
├── models/
│   ├── __init__.py
│   ├── estate_property.py
│   ├── estate_property_offers.py
│   ├── estate_property_type.py
│   └── estate_property_tags.py
│
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
│
└── views/
    ├── estate_menus.xml
    ├── estate_property_views.xml
    ├── estate_property_type_views.xml
    ├── estate_property_tags_views.xml
    └── estate_property_offers_views.xml


estate_account/
├── __init__.py
├── __manifest__.py
│
├── models/
│   ├── __init__.py
│   └── estate_property_inherit.py   # herda estate.property e adiciona integração com account
│
└── views/
    └── estate_account_views.xml
```

---

## 📌 Arquivos principais

### `estate/__init__.py`
```python
from . import models
```

---

### `estate/models/__init__.py`
```python
from . import estate_property
from . import estate_property_offers
from . import estate_property_type
from . import estate_property_tags
```

---

### `estate/__manifest__.py`
```python
{
    'name': "Estate Management",
    'version': '1.0',
    'depends': ['base'],
    'author': "O Seu Nome",
    'category': 'Real Estate',
    'summary': "Gestão de propriedades imobiliárias",
    'application': True,
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_menus.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offers_views.xml',
    ],
}
```

---

### `estate_account/__init__.py`
```python
from . import models
```

---

### `estate_account/models/__init__.py`
```python
from . import estate_property_inherit
```

---

### `estate_account/__manifest__.py`
```python
{
    'name': "Estate Accounting",
    'version': '1.0',
    'depends': ['estate', 'account'],
    'author': "O Seu Nome",
    'category': 'Real Estate',
    'summary': "Integração com Contabilidade para o módulo Estate",
    'application': False,
    'installable': True,
    'data': [
        'views/estate_account_views.xml',
    ],
}
```

---

## 📌 Integração com Contabilidade (`estate_account`)

No módulo `estate_account`, criamos um modelo herdado de `estate.property` que adiciona um método para **gerar faturas** assim que a propriedade é vendida.

### `estate_account/models/estate_property_inherit.py`
```python
from odoo import api, fields, models
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        """Ao vender uma propriedade, gera uma fatura no módulo account."""
        res = super().action_sold()

        move_obj = self.env['account.move']

        for property in self:
            if not property.buyer:
                raise UserError("Não é possível vender sem comprador.")

            # Criar fatura
            invoice = move_obj.create({
                'move_type': 'out_invoice',
                'partner_id': property.buyer.id,
                'invoice_line_ids': [
                    (0, 0, {
                        'name': property.name,
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,  # comissão 6%
                    }),
                    (0, 0, {
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': 100.00,
                    })
                ]
            })

        return res
```

---

## 📌 Segurança

### `estate/security/ir.model.access.csv`
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_estate_property,access.estate.property,model_estate_property,,1,1,1,1
access_estate_property_type,access.estate.property.type,model_estate_property_type,,1,1,1,1
access_estate_property_tags,access.estate.property.tags,model_estate_property_tags,,1,1,1,1
access_estate_property_offers,access.estate.property.offers,model_estate_property_offers,,1,1,1,1
```

---

## 🚀 Instalação

1. Copiar `estate/` e `estate_account/` para a pasta `addons/` do Odoo  
2. Atualizar lista de apps no Odoo (`Aplicações > Atualizar lista de apps`)  
3. Instalar **Estate Management**  
4. (Opcional) Instalar **Estate Accounting** para ativar a integração com contabilidade  

---

## ✅ Resultado esperado

- **Estate Management**: permite gerenciar propriedades, tipos, tags e ofertas.  
- **Estate Accounting**: ao vender uma propriedade, gera automaticamente uma **fatura** no módulo **Contabilidade** com:  
  - 💰 Comissão de 6% sobre o preço da venda  
  - 🧾 Taxa administrativa fixa de 100€  
