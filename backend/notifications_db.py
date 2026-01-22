"""
Módulo para manejar persistencia de configuración de notificaciones en SQLite.
Guarda y recupera credenciales de email y preferencias del usuario.
"""

import sqlite3
import os
from typing import Dict, Optional, Tuple


class NotificationsDB:
    """Gestor de base de datos para configuración de notificaciones."""
    
    DB_PATH = "notifications_config.db"
    
    def __init__(self):
        """Inicializa la base de datos y crea tablas si no existen."""
        self._create_tables()
    
    def _get_connection(self):
        """Obtiene una conexión a la base de datos."""
        return sqlite3.connect(self.DB_PATH)
    
    def _create_tables(self):
        """Crea las tablas si no existen."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Tabla para credenciales de email
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                recipient_email TEXT,
                gmail_user TEXT,
                gmail_app_password TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla para preferencias de notificaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_preferences (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                enabled BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_email_config(
        self,
        recipient_email: str,
        gmail_user: str,
        gmail_app_password: str
    ) -> Tuple[bool, str]:
        """
        Guarda o actualiza la configuración de email.
        
        Parameters:
        -----------
        recipient_email : str
            Correo de destino
        gmail_user : str
            Usuario de Gmail
        gmail_app_password : str
            Contraseña de aplicación Gmail
            
        Returns:
        --------
        tuple
            (success: bool, message: str)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Verificar si existe un registro
            cursor.execute('SELECT id FROM email_config WHERE id = 1')
            exists = cursor.fetchone() is not None
            
            if exists:
                # Actualizar
                cursor.execute('''
                    UPDATE email_config
                    SET recipient_email = ?,
                        gmail_user = ?,
                        gmail_app_password = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = 1
                ''', (recipient_email, gmail_user, gmail_app_password))
            else:
                # Insertar
                cursor.execute('''
                    INSERT INTO email_config (id, recipient_email, gmail_user, gmail_app_password)
                    VALUES (1, ?, ?, ?)
                ''', (recipient_email, gmail_user, gmail_app_password))
            
            conn.commit()
            conn.close()
            
            return True, "✅ Configuración de email guardada exitosamente"
        
        except Exception as e:
            return False, f"❌ Error al guardar configuración: {str(e)}"
    
    def load_email_config(self) -> Dict[str, str]:
        """
        Carga la configuración de email guardada.
        
        Returns:
        --------
        dict
            Diccionario con 'recipient_email', 'gmail_user', 'gmail_app_password'
            Si no existe, devuelve diccionario vacío
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT recipient_email, gmail_user, gmail_app_password
                FROM email_config
                WHERE id = 1
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'recipient_email': result[0] or '',
                    'gmail_user': result[1] or '',
                    'gmail_app_password': result[2] or ''
                }
            else:
                return {
                    'recipient_email': '',
                    'gmail_user': '',
                    'gmail_app_password': ''
                }
        
        except Exception as e:
            print(f"Error al cargar configuración de email: {str(e)}")
            return {
                'recipient_email': '',
                'gmail_user': '',
                'gmail_app_password': ''
            }
    
    def save_preferences(self, enabled: bool) -> Tuple[bool, str]:
        """
        Guarda las preferencias de notificaciones.
        
        Parameters:
        -----------
        enabled : bool
            Si está habilitado o deshabilitado
            
        Returns:
        --------
        tuple
            (success: bool, message: str)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Verificar si existe un registro
            cursor.execute('SELECT id FROM notification_preferences WHERE id = 1')
            exists = cursor.fetchone() is not None
            
            if exists:
                # Actualizar
                cursor.execute('''
                    UPDATE notification_preferences
                    SET enabled = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = 1
                ''', (1 if enabled else 0,))
            else:
                # Insertar
                cursor.execute('''
                    INSERT INTO notification_preferences (id, enabled)
                    VALUES (1, ?)
                ''', (1 if enabled else 0,))
            
            conn.commit()
            conn.close()
            
            return True, "✅ Preferencias guardadas"
        
        except Exception as e:
            return False, f"❌ Error al guardar preferencias: {str(e)}"
    
    def load_preferences(self) -> bool:
        """
        Carga si las notificaciones están habilitadas.
        
        Returns:
        --------
        bool
            True si está habilitado, False si no
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT enabled
                FROM notification_preferences
                WHERE id = 1
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return bool(result[0])
            else:
                return False
        
        except Exception as e:
            print(f"Error al cargar preferencias: {str(e)}")
            return False
    
    def clear_all(self) -> Tuple[bool, str]:
        """
        Elimina toda la configuración guardada (para limpiar datos).
        
        Returns:
        --------
        tuple
            (success: bool, message: str)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM email_config WHERE id = 1')
            cursor.execute('DELETE FROM notification_preferences WHERE id = 1')
            
            conn.commit()
            conn.close()
            
            return True, "✅ Toda la configuración ha sido eliminada"
        
        except Exception as e:
            return False, f"❌ Error al limpiar datos: {str(e)}"
    
    def delete_email_config(self) -> Tuple[bool, str]:
        """
        Elimina solo la configuración de email.
        
        Returns:
        --------
        tuple
            (success: bool, message: str)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM email_config WHERE id = 1')
            
            conn.commit()
            conn.close()
            
            return True, "✅ Configuración de email eliminada"
        
        except Exception as e:
            return False, f"❌ Error al eliminar configuración: {str(e)}"
