"""Utilize o Se Suite com o python!"""

from .sesuite import Entity as Entity
from .sesuite import Relationship as Relationship
from .sesuite import Sesuite as Sesuite
from .sesuite import TableField as TableField

__all__ = ["Entity", "Relationship", "Sesuite", "TableField"]
__version__ = "4.0.3"
