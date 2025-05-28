import logging
import sys

class ColoredFormatter(logging.Formatter):
    """Formateador personalizado que agrega colores a los logs"""
    
    COLORS = {
        'DEBUG': '\033[94m',    # Azul
        'INFO': '\033[92m',     # Verde
        'WARNING': '\033[93m',  # Amarillo
        'ERROR': '\033[91m',    # Rojo
        'CRITICAL': '\033[91m\033[1m', # Rojo negrita
        'RESET': '\033[0m'      # Reset
    }

    SEGMENT_COLORS = {
        'asctime': '\033[36m',  # Cyan claro
        'name': '\033[35m',     # Magenta
        'levelname': '\033[33m', # Amarillo oscuro
        'RESET': '\033[0m'      # Reset
    }

    def format(self, record):
        # Guardar el mensaje original
        original_msg = record.msg
        
        # Agregar color al mensaje según el nivel
        if record.levelname in self.COLORS:
            record.msg = f"{self.COLORS[record.levelname]}{record.msg}{self.COLORS['RESET']}"
        
        # Formatear el mensaje con colores en los segmentos
        formatted = super().format(record)
        
        # Aplicar colores a los segmentos
        formatted = formatted.replace(
            record.asctime,
            f"{self.SEGMENT_COLORS['asctime']}{record.asctime}{self.SEGMENT_COLORS['RESET']}"
        )
        formatted = formatted.replace(
            record.name,
            f"{self.SEGMENT_COLORS['name']}{record.name}{self.SEGMENT_COLORS['RESET']}"
        )
        formatted = formatted.replace(
            record.levelname,
            f"{self.SEGMENT_COLORS['levelname']}{record.levelname}{self.SEGMENT_COLORS['RESET']}"
        )
        
        # Restaurar el mensaje original
        record.msg = original_msg
        
        return formatted

def setup_logger(name: str) -> logging.Logger:
    # Crear el logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Configurar el formato del log
    formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


    # Handler para consola (con colores)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger