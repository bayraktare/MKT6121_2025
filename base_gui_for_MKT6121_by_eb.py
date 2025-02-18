import sys, cv2, os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                           QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget,
                           QFileDialog, QCheckBox, QComboBox, QScrollArea,
                           QGroupBox, QGridLayout, QSpinBox, QDoubleSpinBox,
                           QStatusBar, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QIcon
import numpy as np

class ImageProcessingGUI(QMainWindow):
    """
    Main GUI class for the image processing application.
    Students will extend this class by implementing various image processing methods.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Advanced Image Processing Suite")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        
        # Initialize all UI components
        self.create_menu_bar()
        self.create_toolbar()
        self.create_input_section()
        self.create_image_display()
        self.create_method_tabs()
        self.create_control_panel()
        self.create_status_bar()
        
        # Initialize state variables
        self.current_image = None
        self.processed_image = None
        self.video_capture = None
        self.processing_history = []
        
        # Setup video/webcam timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        
    def create_menu_bar(self):
        """Create the menu bar with File, Edit, View, and Help menus"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        actions = [
            ("Open Image", self.open_image),
            ("Open Video", self.open_video),
            ("Save Result", self.save_result),
            ("Export History", self.export_history),
            ("Exit", self.close)
        ]
        for text, slot in actions:
            action = file_menu.addAction(text)
            action.triggered.connect(slot)
            
        # Add other menus (Edit, View, Help) as needed
        
    def create_toolbar(self):
        """Create the toolbar with quick access buttons"""
        toolbar = self.addToolBar("Tools")
        toolbar.setMovable(False)
        
        # Add tool buttons
        self.add_toolbar_button(toolbar, "Open", self.open_image)
        self.add_toolbar_button(toolbar, "Save", self.save_result)
        self.add_toolbar_button(toolbar, "Reset", self.reset_processing)
        toolbar.addSeparator()
        self.add_toolbar_button(toolbar, "Zoom In", self.zoom_in)
        self.add_toolbar_button(toolbar, "Zoom Out", self.zoom_out)
        
    def create_input_section(self):
        """Create the input source selection section"""
        input_group = QGroupBox("Input Source")
        input_layout = QHBoxLayout()
        
        # Source selection combo
        self.source_combo = QComboBox()
        self.source_combo.addItems(["Single Image", "Video File", "Webcam"])
        self.source_combo.currentTextChanged.connect(self.change_source)
        
        # Source selection button
        self.select_source_btn = QPushButton("Select Source")
        self.select_source_btn.clicked.connect(self.select_source)
        
        # Add widgets to layout
        input_layout.addWidget(QLabel("Source Type:"))
        input_layout.addWidget(self.source_combo)
        input_layout.addWidget(self.select_source_btn)
        input_layout.addStretch()
        
        # Create resolution control for webcam
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["640x480", "1280x720", "1920x1080"])
        self.resolution_combo.setVisible(False)
        input_layout.addWidget(QLabel("Resolution:"))
        input_layout.addWidget(self.resolution_combo)
        
        input_group.setLayout(input_layout)
        self.main_layout.addWidget(input_group)
        
    def create_image_display(self):
        """Create the image display area with input and output views"""
        display_layout = QHBoxLayout()
        
        # Input image section
        input_group = QGroupBox("Input Image")
        input_layout = QVBoxLayout()
        self.input_scroll = QScrollArea()
        self.input_image_label = QLabel()
        self.input_image_label.setMinimumSize(500, 400)
        self.input_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_scroll.setWidget(self.input_image_label)
        self.input_scroll.setWidgetResizable(True)
        input_layout.addWidget(self.input_scroll)
        input_group.setLayout(input_layout)
        
        # Output image section
        output_group = QGroupBox("Processed Image")
        output_layout = QVBoxLayout()
        self.output_scroll = QScrollArea()
        self.output_image_label = QLabel()
        self.output_image_label.setMinimumSize(500, 400)
        self.output_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.output_scroll.setWidget(self.output_image_label)
        self.output_scroll.setWidgetResizable(True)
        output_layout.addWidget(self.output_scroll)
        output_group.setLayout(output_layout)
        
        display_layout.addWidget(input_group)
        display_layout.addWidget(output_group)
        self.main_layout.addLayout(display_layout)
        
    def create_method_tabs(self):
        """Create tabs for different processing method categories"""
        self.tab_widget = QTabWidget()
        
        # Create tabs with scroll areas
        tabs_data = [
            ("Classical Methods", self.create_classical_tab),
            ("Geometric Methods", self.create_geometric_tab),
            ("Modern Methods", self.create_modern_tab)
        ]
        
        for tab_name, create_func in tabs_data:
            scroll = QScrollArea()
            tab_widget = create_func()
            scroll.setWidget(tab_widget)
            scroll.setWidgetResizable(True)
            self.tab_widget.addTab(scroll, tab_name)
        
        self.main_layout.addWidget(self.tab_widget)
        
    def create_classical_tab(self):
        """Create the classical methods tab content"""
        widget = QWidget()
        layout = QGridLayout(widget)
        
        # Example method groups (students will implement these)
        groups = [
            ("Filtering", ["Gaussian Blur", "Median Filter", "Bilateral Filter"]),
            ("Edge Detection", ["Sobel", "Canny", "Laplacian"]),
            ("Morphological", ["Erosion", "Dilation", "Opening", "Closing"])
        ]
        
        for i, (group_name, methods) in enumerate(groups):
            group = QGroupBox(group_name)
            group_layout = QVBoxLayout()
            
            for method in methods:
                checkbox = QCheckBox(method)
                checkbox.setEnabled(False)  # Initially disabled
                group_layout.addWidget(checkbox)
            
            group.setLayout(group_layout)
            layout.addWidget(group, i // 2, i % 2)
        
        return widget
        
    def create_geometric_tab(self):
        """Create the geometric methods tab content"""
        widget = QWidget()
        layout = QGridLayout(widget)
        
        # Example geometric operations (students will implement these)
        groups = [
            ("Basic Transforms", ["Resize", "Rotate", "Flip"]),
            ("Advanced Transforms", ["Affine", "Perspective", "Warp"]),
            ("Features", ["Corner Detection", "Line Detection", "Contours"])
        ]
        
        for i, (group_name, methods) in enumerate(groups):
            group = QGroupBox(group_name)
            group_layout = QVBoxLayout()
            
            for method in methods:
                checkbox = QCheckBox(method)
                checkbox.setEnabled(False)  # Initially disabled
                group_layout.addWidget(checkbox)
            
            group.setLayout(group_layout)
            layout.addWidget(group, i // 2, i % 2)
        
        return widget
        
    def create_modern_tab(self):
        """Create the modern methods tab content"""
        widget = QWidget()
        layout = QGridLayout(widget)
        
        # Example modern techniques (students will implement these)
        groups = [
            ("Enhancement", ["Histogram Equalization", "Contrast Stretching"]),
            ("Segmentation", ["Threshold", "K-means", "Watershed"]),
            ("Feature Extraction", ["SIFT", "SURF", "ORB"])
        ]
        
        for i, (group_name, methods) in enumerate(groups):
            group = QGroupBox(group_name)
            group_layout = QVBoxLayout()
            
            for method in methods:
                checkbox = QCheckBox(method)
                checkbox.setEnabled(False)  # Initially disabled
                group_layout.addWidget(checkbox)
            
            group.setLayout(group_layout)
            layout.addWidget(group, i // 2, i % 2)
        
        return widget
        
    def create_control_panel(self):
        """Create the bottom control panel"""
        control_group = QGroupBox("Processing Controls")
        control_layout = QHBoxLayout()
        
        # Processing options
        self.additive_checkbox = QCheckBox("Additive Operations")
        self.live_preview_checkbox = QCheckBox("Live Preview")
        
        # Control buttons
        self.process_btn = QPushButton("Process")
        self.process_btn.clicked.connect(self.process_image)
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_processing)
        self.undo_btn = QPushButton("Undo")
        self.undo_btn.clicked.connect(self.undo_last_operation)
        
        # Add widgets to layout
        control_layout.addWidget(self.additive_checkbox)
        control_layout.addWidget(self.live_preview_checkbox)
        control_layout.addStretch()
        control_layout.addWidget(self.undo_btn)
        control_layout.addWidget(self.process_btn)
        control_layout.addWidget(self.reset_btn)
        
        control_group.setLayout(control_layout)
        self.main_layout.addWidget(control_group)
        
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Add image info label
        self.image_info_label = QLabel()
        self.status_bar.addPermanentWidget(self.image_info_label)
        
    def add_toolbar_button(self, toolbar, text, slot):
        """Helper method to add buttons to toolbar"""
        button = QPushButton(text)
        button.clicked.connect(slot)
        toolbar.addWidget(button)
        
    def select_source(self):
        """Handle source selection based on combo box choice"""
        source_type = self.source_combo.currentText()
        try:
            if source_type == "Single Image":
                self.open_image()
            elif source_type == "Video File":
                self.open_video()
            elif source_type == "Webcam":
                self.start_webcam()
        except Exception as e:
            self.show_error(f"Error selecting source: {str(e)}")
            
    def open_image(self):
        """Open and load an image file"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        if file_name:
            try:
                self.load_image(file_name)
                self.status_bar.showMessage(f"Loaded image: {os.path.basename(file_name)}")
            except Exception as e:
                self.show_error(f"Error loading image: {str(e)}")
                
    def open_video(self):
        """Open and load a video file"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video",
            "",
            "Videos (*.mp4 *.avi *.mov *.mkv)"
        )
        if file_name:
            try:
                self.start_video(file_name)
                self.status_bar.showMessage(f"Playing video: {os.path.basename(file_name)}")
            except Exception as e:
                self.show_error(f"Error loading video: {str(e)}")
                
    def start_webcam(self):
        """Initialize and start webcam capture"""
        try:
            self.video_capture = cv2.VideoCapture(0)
            if self.video_capture.isOpened():
                # Set resolution based on combo box
                resolution = self.resolution_combo.currentText()
                width, height = map(int, resolution.split('x'))
                self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                
                self.timer.start(30)  # 30ms refresh rate
                self.status_bar.showMessage("Webcam started")
            else:
                raise Exception("Could not open webcam")
        except Exception as e:
            self.show_error(f"Error starting webcam: {str(e)}")
            
    def change_source(self):
        """Handle source type change"""
        if self.video_capture is not None:
            self.video_capture.release()
            self.timer.stop()
        self.reset_processing()
        self.resolution_combo.setVisible(self.source_combo.currentText() == "Webcam")
        
    def load_image(self, file_name):
        """Load and display an image file"""
        self.current_image = cv2.imread(file_name)
        if self.current_image is None:
            raise Exception("Could not load image")
        
        self.processed_image = self.current_image.copy()
        self.display_image(self.current_image, self.input_image_label)
        self.display_image(self.current_image, self.output_image_label)
        self.update_image_info()
        
    def start_video(self, file_name):
        """Start video playback"""
        self.video_capture = cv2.VideoCapture(file_name)
        if not self.video_capture.isOpened():
            raise Exception("Could not open video file")
        self.timer.start(30)
        
    def update_frame(self):
        """Update frame for video/webcam display"""
        ret, frame = self.video_capture.read()
        if ret:
            self.current_image = frame
            self.processed_image = frame.copy()
            self.display_image(frame, self.input_image_label)
            if self.live_preview_checkbox.isChecked():
                self.process_image()
            else:
                self.display_image(frame, self.output_image_label)
            self.update_image_info()
        else:
            # Video ended or frame grab failed
            self.timer.stop()
            if self.video_capture is not None:
                self.video_capture.release()
                self.video_capture = None
            self.status_bar.showMessage("Video ended")

    def display_image(self, image, label):
        """Display an image on a QLabel with proper scaling"""
        if image is not None:
            height, width = image.shape[:2]
            label_width = label.width()
            label_height = label.height()
            
            # Calculate aspect ratio preserving scaling
            aspect_ratio = width / height
            if label_width / aspect_ratio <= label_height:
                new_width = label_width
                new_height = int(label_width / aspect_ratio)
            else:
                new_height = label_height
                new_width = int(label_height * aspect_ratio)
            
            # Convert the image to RGB format
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            
            # Create QImage and QPixmap
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(new_width, new_height, 
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            label.setPixmap(scaled_pixmap)

    def process_image(self):
        """Process the image with selected methods"""
        if self.current_image is None:
            self.show_error("No image loaded")
            return
            
        try:
            # Make a copy of the input image
            if not self.additive_checkbox.isChecked():
                self.processed_image = self.current_image.copy()
            
            # Students will implement their processing methods here
            # This is a placeholder for demonstration
            self.status_bar.showMessage("Processing image...")
            
            # Update the display
            self.display_image(self.processed_image, self.output_image_label)
            self.processing_history.append(self.processed_image.copy())
            
            self.status_bar.showMessage("Processing complete")
            
        except Exception as e:
            self.show_error(f"Error processing image: {str(e)}")

    def reset_processing(self):
        """Reset the processed image to the original"""
        if self.current_image is not None:
            self.processed_image = self.current_image.copy()
            self.display_image(self.processed_image, self.output_image_label)
            self.processing_history.clear()
            self.status_bar.showMessage("Processing reset")

    def undo_last_operation(self):
        """Undo the last processing operation"""
        if len(self.processing_history) > 0:
            self.processed_image = self.processing_history.pop()
            self.display_image(self.processed_image, self.output_image_label)
            self.status_bar.showMessage("Undo last operation")
        else:
            self.status_bar.showMessage("Nothing to undo")

    def save_result(self):
        """Save the processed image"""
        if self.processed_image is None:
            self.show_error("No processed image to save")
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        if file_name:
            try:
                cv2.imwrite(file_name, self.processed_image)
                self.status_bar.showMessage(f"Image saved as: {os.path.basename(file_name)}")
            except Exception as e:
                self.show_error(f"Error saving image: {str(e)}")

    def export_history(self):
        """Export processing history as a series of images"""
        if not self.processing_history:
            self.show_error("No processing history to export")
            return
            
        directory = QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if directory:
            try:
                for i, image in enumerate(self.processing_history):
                    filename = os.path.join(directory, f"step_{i+1}.png")
                    cv2.imwrite(filename, image)
                self.status_bar.showMessage(f"Processing history exported to: {directory}")
            except Exception as e:
                self.show_error(f"Error exporting history: {str(e)}")

    def update_image_info(self):
        """Update image information in status bar"""
        if self.current_image is not None:
            height, width = self.current_image.shape[:2]
            channels = self.current_image.shape[2] if len(self.current_image.shape) > 2 else 1
            size_mb = self.current_image.nbytes / (1024 * 1024)
            self.image_info_label.setText(
                f"Size: {width}x{height} | Channels: {channels} | Memory: {size_mb:.1f}MB"
            )

    def zoom_in(self):
        """Zoom in on the images"""
        # Implement zoom functionality
        pass

    def zoom_out(self):
        """Zoom out of the images"""
        # Implement zoom functionality
        pass

    def show_error(self, message):
        """Show error message in a dialog box"""
        QMessageBox.critical(self, "Error", message)

    def closeEvent(self, event):
        """Handle application closing"""
        if self.video_capture is not None:
            self.video_capture.release()
            self.timer.stop()
        event.accept()

def main():
    """Main function to start the application"""
    app = QApplication(sys.argv)
    window = ImageProcessingGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()