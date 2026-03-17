# Serializuje i deserializuje obiekty domenowe (np. konfiguracje, wyniki)
# src/ga_optimizer/io/serializers.py

import json
from typing import Any

class SafeJSONEncoder(json.JSONEncoder):
    """
    Niestandardowy enkoder JSON zabezpieczający przed błędami serializacji
    dla obiektów takich jak instancje generatorów losowych (rng) itp.
    """
    def default(self, obj: Any) -> Any:
        try:
            return super().default(obj)
        except TypeError:
            # Jeśli obiekt nie jest wspierany przez JSON, zamień go na string
            return str(obj)
