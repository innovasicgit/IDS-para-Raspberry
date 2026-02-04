"""
Módulo para manejar notificaciones por correo y en la interfaz de Streamlit.
Incluye lógica inteligente para no saturar al usuario con demasiadas notificaciones.
"""

import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Optional


class NotificationManager:
    """Gestor de notificaciones con control de frecuencia inteligente."""
    
    def __init__(self):
        self.alert_state = {
            'last_email_timestamp': 0,
            'normal_email_interval': 1800,      # 30 minutos para estado normal
            'attack_email_interval': 300,       # 5 minutos para estado de ataque
            'previous_state': 'normal',         # 'normal' o 'attack'
            'attack_started': None,             # Timestamp cuando comenzó el ataque
            'normal_since': None,               # Timestamp cuando terminó el ataque
            'anomaly_percentage': 0
        }
    
    def get_alert_level(self, anomaly_percentage: float) -> str:
        """
        Determina el nivel de alerta según el porcentaje de anomalías.
        
        Parameters:
        -----------
        anomaly_percentage : float
            Porcentaje de anomalías detectadas (0-100)
            
        Returns:
        --------
        str
            'normal' (<30%), 'suspicious' (30-80%), 'attack' (>=80%)
        """
        if anomaly_percentage >= 80:
            return 'attack'
        elif anomaly_percentage >= 45:
            return 'suspicious'
        else:
            return 'normal'
    
    def should_send_email(self, anomaly_percentage: float) -> bool:
        """
        Determina si se debe enviar email basado en el estado actual y el historial.
        
        Parameters:
        -----------
        anomaly_percentage : float
            Porcentaje de anomalías detectadas (0-100)
            
        Returns:
        --------
        bool
            True si se debe enviar email, False en otro caso
        """
        current_time = time.time()
        previous_state = self.alert_state['previous_state']
        current_state = self.get_alert_level(anomaly_percentage)
        
        # Cambio de estado: siempre enviar email
        if current_state != previous_state:
            self.alert_state['previous_state'] = current_state
            self.alert_state['last_email_timestamp'] = current_time
            
            if current_state == 'attack':
                self.alert_state['attack_started'] = current_time
            elif current_state == 'normal' and previous_state in ['attack', 'suspicious']:
                self.alert_state['normal_since'] = current_time
            
            return True
        
        # Sin cambio de estado: verificar intervalos
        if current_state == 'attack':
            interval = self.alert_state['attack_email_interval']  # 5 minutos
        elif current_state == 'suspicious':
            interval = 600  # 10 minutos para estado sospechoso
        else:
            interval = self.alert_state['normal_email_interval']  # 30 minutos
        
        time_since_last_email = current_time - self.alert_state['last_email_timestamp']
        
        if time_since_last_email >= interval:
            self.alert_state['last_email_timestamp'] = current_time
            return True
        
        return False
    
    def get_alert_message(self, anomaly_percentage: float, is_manual: bool) -> Dict[str, str]:
        """
        Genera el mensaje de alerta según el contexto.
        
        Parameters:
        -----------
        anomaly_percentage : float
            Porcentaje de anomalías detectadas (0-100)
        is_manual : bool
            True si es captura manual, False si es automática
            
        Returns:
        --------
        dict
            Diccionario con 'title', 'message', 'type' ('success', 'warning', 'error')
        """
        alert_level = self.get_alert_level(anomaly_percentage)
        
        if alert_level == 'attack':
            return {
                'title': '🚨 ALERTA CRÍTICA DE SEGURIDAD',
                'message': f'⚠️ Posible ataque detectado: {anomaly_percentage:.1f}% anomalías',
                'type': 'error'
            }
        elif alert_level == 'suspicious':
            return {
                'title': '⚠️ ALERTA MEDIA - Actividad Sospechosa',
                'message': f'🔍 Tráfico anómalo detectado: {anomaly_percentage:.1f}% anomalías. Monitoreo recomendado.',
                'type': 'warning'
            }
        else:
            return {
                'title': '✅ Estado Normal',
                'message': f'Tráfico normal ({anomaly_percentage:.1f}% anomalías detectadas)',
                'type': 'success'
            }
    
    def get_email_subject_and_body(
        self, 
        anomaly_percentage: float, 
        is_manual: bool = False,
        model_name: str = 'IForest',
        timestamp: Optional[datetime] = None
    ) -> tuple:
        """
        Genera asunto y cuerpo del email HTML.
        
        Parameters:
        -----------
        anomaly_percentage : float
            Porcentaje de anomalías
        is_manual : bool
            Si es captura manual
        model_name : str
            Nombre del modelo usado
        timestamp : datetime
            Timestamp de la predicción
            
        Returns:
        --------
        tuple
            (asunto, cuerpo_html)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        alert_level = self.get_alert_level(anomaly_percentage)
        
        if alert_level == 'attack':
            subject = f"🚨 ALERTA IDS: POSIBLE ATAQUE DETECTADO - {timestamp.strftime('%d/%m/%Y %H:%M')}"
            
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4444;">
                        <h2 style="color: #ff4444;">🚨 ALERTA CRÍTICA DE SEGURIDAD</h2>
                        <p style="color: #333; font-size: 16px;">
                            <strong>Se ha detectado posible actividad de ataque en tu red.</strong>
                        </p>
                        
                        <div style="background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p><strong>Anomalías detectadas:</strong> <span style="color: #ff4444; font-size: 20px;">{anomaly_percentage:.1f}%</span></p>
                            <p><strong>Nivel de alerta:</strong> <span style="color: #ff4444; font-weight: bold;">CRÍTICO (≥80%)</span></p>
                            <p><strong>Modelo utilizado:</strong> {model_name}</p>
                            <p><strong>Fecha y hora:</strong> {timestamp.strftime('%d/%m/%Y %H:%M:%S')}</p>
                            <p><strong>Tipo de captura:</strong> {'Manual' if is_manual else 'Automática'}</p>
                        </div>
                        
                        <p style="color: #333;">
                            <strong>Acciones recomendadas:</strong>
                        </p>
                        <ul style="color: #333;">
                            <li>Accede inmediatamente a la consola del IDS</li>
                            <li>Revisa los detalles de las anomalías detectadas</li>
                            <li>Toma medidas preventivas si es necesario</li>
                            <li>Aumenta la supervisión de tu red</li>
                        </ul>
                        
                        <p style="color: #666; font-size: 12px; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px;">
                            Este es un mensaje automático del Sistema de Detección de Anomalías (IDS).
                        </p>
                    </div>
                </body>
            </html>
            """
        elif alert_level == 'suspicious':
            subject = f"⚠️ ALERTA IDS: ACTIVIDAD SOSPECHOSA - {timestamp.strftime('%d/%m/%Y %H:%M')}"
            
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #ff9800;">
                        <h2 style="color: #ff9800;">⚠️ ALERTA MEDIA - Actividad Sospechosa</h2>
                        <p style="color: #333; font-size: 16px;">
                            <strong>Se ha detectado tráfico anómalo en tu red que supera los niveles normales.</strong>
                        </p>
                        
                        <div style="background-color: #fff3e0; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p><strong>Anomalías detectadas:</strong> <span style="color: #ff9800; font-size: 20px;">{anomaly_percentage:.1f}%</span></p>
                            <p><strong>Nivel de alerta:</strong> <span style="color: #ff9800; font-weight: bold;">MEDIO (30-80%)</span></p>
                            <p><strong>Modelo utilizado:</strong> {model_name}</p>
                            <p><strong>Fecha y hora:</strong> {timestamp.strftime('%d/%m/%Y %H:%M:%S')}</p>
                            <p><strong>Tipo de captura:</strong> {'Manual' if is_manual else 'Automática'}</p>
                        </div>
                        
                        <p style="color: #333;">
                            <strong>Acciones recomendadas:</strong>
                        </p>
                        <ul style="color: #333;">
                            <li>Monitorear la red de cerca para detectar posibles escalaciones</li>
                            <li>Revisar los patrones de tráfico en la consola del IDS</li>
                            <li>Verificar si hay actividades inusuales de usuarios o servicios</li>
                            <li>Considerar aumentar la frecuencia de captura para análisis más detallado</li>
                        </ul>
                        
                        <p style="color: #666; font-size: 14px; margin-top: 20px;">
                            <strong>Nota:</strong> Este nivel de anomalías indica un comportamiento que no es normal pero tampoco crítico.
                            Puede tratarse de ataques de baja intensidad, reconocimiento de red o configuraciones incorrectas.
                        </p>
                        
                        <p style="color: #666; font-size: 12px; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px;">
                            Este es un mensaje automático del Sistema de Detección de Anomalías (IDS).
                        </p>
                    </div>
                </body>
            </html>
            """
        else:
            subject = f"✅ IDS: Estado Normal - {timestamp.strftime('%d/%m/%Y %H:%M')}"
            
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 10px; border-left: 5px solid #44aa44;">
                        <h2 style="color: #44aa44;">✅ ESTADO NORMAL</h2>
                        <p style="color: #333; font-size: 16px;">
                            <strong>Tu red se encuentra en estado normal.</strong>
                        </p>
                        
                        <div style="background-color: #e8f5e9; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <p><strong>Anomalías detectadas:</strong> <span style="color: #44aa44; font-size: 20px;">{anomaly_percentage:.1f}%</span></p>
                            <p><strong>Nivel de alerta:</strong> <span style="color: #44aa44; font-weight: bold;">NORMAL (<30%)</span></p>
                            <p><strong>Modelo utilizado:</strong> {model_name}</p>
                            <p><strong>Fecha y hora:</strong> {timestamp.strftime('%d/%m/%Y %H:%M:%S')}</p>
                            <p><strong>Tipo de captura:</strong> {'Manual' if is_manual else 'Automática'}</p>
                        </div>
                        
                        <p style="color: #333;">
                            Los patrones detectados son consistentes con tráfico normal de la red.
                            El pequeño porcentaje de anomalías probablemente se debe al margen de error del modelo.
                        </p>
                        
                        <p style="color: #666; font-size: 12px; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px;">
                            Este es un mensaje automático del Sistema de Detección de Anomalías (IDS).
                        </p>
                    </div>
                </body>
            </html>
            """
        
        return subject, body
    
    def send_email(
        self,
        recipient_email: str,
        gmail_user: str,
        gmail_password: str,
        anomaly_percentage: float,
        is_manual: bool = False,
        model_name: str = 'IForest'
    ) -> tuple:
        """
        Envía un email con la notificación de alerta.
        
        Parameters:
        -----------
        recipient_email : str
            Correo del destinatario
        gmail_user : str
            Usuario de Gmail
        gmail_password : str
            Contraseña de aplicación de Gmail
        anomaly_percentage : float
            Porcentaje de anomalías
        is_manual : bool
            Si es captura manual
        model_name : str
            Nombre del modelo
            
        Returns:
        --------
        tuple
            (success: bool, message: str)
        """
        try:
            # Crear mensaje
            timestamp = datetime.now()
            subject, html_body = self.get_email_subject_and_body(
                anomaly_percentage, 
                is_manual, 
                model_name,
                timestamp
            )
            
            # Configurar mensaje MIME
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = gmail_user
            message['To'] = recipient_email
            
            # Agregar cuerpo HTML
            message.attach(MIMEText(html_body, 'html'))
            
            # Conectar a Gmail SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            
            # Enviar email
            server.send_message(message)
            server.quit()
            
            return True, f"Email enviado exitosamente a {recipient_email}"
        
        except smtplib.SMTPAuthenticationError:
            return False, "Error de autenticación. Verifica usuario/contraseña de Gmail"
        except smtplib.SMTPException as e:
            return False, f"Error SMTP: {str(e)}"
        except Exception as e:
            return False, f"Error al enviar email: {str(e)}"
    
    def update_state(self, anomaly_percentage: float):
        """
        Actualiza el estado interno con el porcentaje de anomalías.
        
        Parameters:
        -----------
        anomaly_percentage : float
            Porcentaje de anomalías detectadas
        """
        self.alert_state['anomaly_percentage'] = anomaly_percentage
    
    def reset_state(self):
        """Reinicia el estado de alertas."""
        self.__init__()
