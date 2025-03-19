import sys
import time
import logging
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                              QTextEdit, QPushButton, QCheckBox, QFileDialog)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QTextCursor, QPalette

class LogHandler(logging.Handler):
    """Custom logging handler that sends logs to the terminal window"""
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        
    def emit(self, record):
        log_entry = self.format(record)
        self.callback(log_entry, record.levelno)

class LogTerminal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Application Log Terminal")
        self.resize(800, 500)
        
        # Store original window flags
        self.original_flags = self.windowFlags()
        
        self.init_ui()
        
        # Set up logging
        self.log_handler = LogHandler(self.append_log)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(formatter)
        
        # Center the window relative to parent if provided
        if parent:
            parent_geometry = parent.geometry()
            self_size = self.size()
            x = parent_geometry.x() + (parent_geometry.width() - self_size.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self_size.height()) // 2
            self.move(x, y)
            
        # Add initial message
        self.append_log("Log Terminal started", logging.INFO)
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_logs)
        
        self.save_button = QPushButton("Save Logs")
        self.save_button.clicked.connect(self.save_logs)
        
        self.autoscroll_checkbox = QCheckBox("Auto-scroll")
        self.autoscroll_checkbox.setChecked(True)
        
        self.always_on_top_button = QPushButton("Always on Top: Off")
        self.always_on_top_button.setCheckable(True)
        self.always_on_top_button.clicked.connect(self.toggle_always_on_top)
        
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.save_button)
        controls_layout.addWidget(self.autoscroll_checkbox)
        controls_layout.addWidget(self.always_on_top_button)
        controls_layout.addStretch()
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Courier New", 10))
        self.log_display.setLineWrapMode(QTextEdit.NoWrap)
        
        # Set dark background with white text
        palette = self.log_display.palette()
        palette.setColor(QPalette.Base, QColor(30, 30, 30))  # Dark background
        palette.setColor(QPalette.Text, QColor(220, 220, 220))  # Light gray text
        self.log_display.setPalette(palette)
        
        # Add widgets to layout
        layout.addLayout(controls_layout)
        layout.addWidget(self.log_display)
        
        self.setLayout(layout)
    
    def toggle_always_on_top(self):
        """Toggle the always-on-top state of the window"""
        # Store current position and size
        current_pos = self.pos()
        current_size = self.size()
        
        # Instead of modifying flags, create a new window with desired flags
        if self.always_on_top_button.isChecked():
            # Use a completely different approach - hide and recreate with new flags
            self.hide()
            self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            self.show()
            self.move(current_pos)
            self.resize(current_size)
            self.always_on_top_button.setText("Always on Top: On")
            self.append_log("Terminal set to always on top", logging.INFO)
        else:
            # Turn off the always-on-top flag
            self.hide()
            self.setWindowFlag(Qt.WindowStaysOnTopHint, False)
            self.show()
            self.move(current_pos)
            self.resize(current_size)
            self.always_on_top_button.setText("Always on Top: Off")
            self.append_log("Terminal no longer always on top", logging.INFO)
    
    def append_log(self, message, level=logging.INFO):
        """Add a log message to the display with appropriate color"""
        # Define colors for different log levels (on dark background)
        colors = {
            logging.DEBUG: QColor(150, 150, 150),    # Light Gray
            logging.INFO: QColor(220, 220, 220),     # White
            logging.WARNING: QColor(255, 200, 0),    # Yellow
            logging.ERROR: QColor(255, 100, 100),    # Light Red
            logging.CRITICAL: QColor(255, 50, 255)   # Pink
        }
        
        # Get the color for this log level
        color = colors.get(level, QColor(220, 220, 220))
        
        # Set text color
        self.log_display.setTextColor(color)
        
        # Add the log message
        self.log_display.append(message)
        
        # Auto-scroll to the bottom if enabled
        if self.autoscroll_checkbox.isChecked():
            self.log_display.moveCursor(QTextCursor.End)
    
    def clear_logs(self):
        """Clear the log display"""
        self.log_display.clear()
        self.append_log("Logs cleared", logging.INFO)
    
    def save_logs(self):
        """Save logs to a file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Logs", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_display.toPlainText())
                self.append_log(f"Logs saved to {filename}", logging.INFO)
            except Exception as e:
                self.append_log(f"Error saving logs: {str(e)}", logging.ERROR)
    
    def get_log_handler(self):
        """Return the log handler for connecting to application loggers"""
        return self.log_handler
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Remove the log handler from any loggers it's attached to
        root_logger = logging.getLogger()
        if self.log_handler in root_logger.handlers:
            root_logger.removeHandler(self.log_handler)
            
        event.accept()


# For testing the module independently
if __name__ == "__main__":
    app = QApplication(sys.argv)
    terminal = LogTerminal()
    
    # Set up a testxyz logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(terminal.get_log_handler())
    
    # Add some testxyz logs
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Show the terminal
    terminal.show()
    
    # Add more logs every few seconds
    def add_log():
        logger.info(f"Current time: {time.strftime('%H:%M:%S')}")
    
    timer = QTimer()
    timer.timeout.connect(add_log)
    timer.start(3000)
    
    sys.exit(app.exec())
