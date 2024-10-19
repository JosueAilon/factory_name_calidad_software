#Básicamente utilizamos un método abstracto llamado factory_method, que posteriormente será implementado por subclases para crear distintos tipos de objetos que en este caso son los productos, las subclases lo podemos ver como notificaciones por email, sms o push. 
#Utilizar este método es útil para la extensibilidad, usarlo para otro producto que en este caso se podría usar en notificaciones WhatsApp, creando una nueva clase sin modificar el código existente. 
#También es útil en reutilización de código, contiene la lógica reutilizable para que funcione en cualquier tipo de producto, mientras que las subclases se encargan de la creación especifica de algún producto. 


from abc import ABC, abstractmethod
from typing import Type


# Interfaz Creador Abstracto
class NotificationCreator(ABC):
    """
    El creador declara el factory method que retornará una notificación específica.
    Ahora, permite la inyección de dependencias para mayor flexibilidad.
    """

    def __init__(self, notification_class: Type['Notification']):
        self._notification_class = notification_class

    def factory_method(self) -> 'Notification':
        """
        Método Factory que retorna una instancia de la clase de notificación.
        """
        return self._notification_class()

    def send_notification(self, recipient: str, message: str) -> str:
        """
        Usa la notificación creada para enviar el mensaje.
        """
        notification = self.factory_method()
        result = notification.send(recipient, message)
        return result


# Interfaz Producto (Notificación abstracta)
class Notification(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> str:
        """
        Método abstracto que las notificaciones concretas implementan para enviar mensajes.
        """
        pass


# Productos Concretos
class EmailNotification(Notification):
    def send(self, recipient: str, message: str) -> str:
        if not recipient or not message:
            raise ValueError("El destinatario o el mensaje no pueden estar vacíos.")
        return f"Email enviado a {recipient}: {message}"


class SMSNotification(Notification):
    def send(self, recipient: str, message: str) -> str:
        if not recipient.startswith("+"):
            raise ValueError("El número de teléfono debe tener el prefijo internacional.")
        if not message:
            raise ValueError("El mensaje no puede estar vacío.")
        return f"SMS enviado a {recipient}: {message}"


class PushNotification(Notification):
    def send(self, recipient: str, message: str) -> str:
        if not recipient or not message:
            raise ValueError("El destinatario o el mensaje no pueden estar vacíos.")
        return f"Notificación Push enviada a {recipient}: {message}"


class SocialMediaNotification(Notification):
    def send(self, recipient: str, message: str) -> str:
        if not recipient or not message:
            raise ValueError("El destinatario o el mensaje no pueden estar vacíos.")
        return f"Mensaje enviado por redes sociales a {recipient}: {message}"


# Código cliente
def client_code(creator: NotificationCreator, recipient: str, message: str):
    """
    El cliente trabaja con el creador abstracto, sin conocer las clases concretas
    de las notificaciones. Simplemente, invoca el método para enviar la notificación.
    """
    try:
        print(creator.send_notification(recipient, message))
    except ValueError as e:
        print(f"Error: {e}")


# Uso del código
if __name__ == "__main__":
    print("Notificación por Email:")
    client_code(NotificationCreator(EmailNotification), "correo@ejemplo.com", "Este es un mensaje importante.")
    
    print("\nNotificación por SMS:")
    client_code(NotificationCreator(SMSNotification), "+123456789", "Este es un mensaje importante.")
    
    print("\nNotificación Push:")
    client_code(NotificationCreator(PushNotification), "usuario_app_123", "Este es un mensaje importante.")
    
    print("\nNotificación por Redes Sociales:")
    client_code(NotificationCreator(SocialMediaNotification), "@usuario_social", "Este es un mensaje importante.")
