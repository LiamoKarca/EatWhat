import os
import random
import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl, QTimer, QDateTime
from PyQt5.QtGui import QDesktopServices, QPixmap, QIcon, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDialog, QScrollArea, \
    QDesktopWidget, QFrame, QFrame, QGraphicsDropShadowEffect, QProgressBar

from Crawler import get_restaurants


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class RestaurantLoader(QThread):
    restaurants_loaded = pyqtSignal(list)

    def run(self):
        print("Fetching restaurant information...")
        restaurants = get_restaurants()
        print("Restaurant information fetched!")
        self.restaurants_loaded.emit(restaurants)


class RestaurantRecommender(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Eat What?")
        self.setFixedSize(720, 680)  # Set window size to 720x680
        self.setStyleSheet("margin: 0; padding: 0;")

        self.set_background_image(get_resource_path("UI/img/background3.png"))
        self.setWindowIcon(QIcon(get_resource_path("UI/img/icon/icon.png")))

        layout = QVBoxLayout()

        # Create time prefix label and set its style
        self.time_prefix_label = QLabel("Current time:", self)
        self.time_prefix_label.setStyleSheet("margin: 5px;")
        self.time_prefix_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Create time label and set its style
        self.time_label = QLabel("", self)
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignTop)

        # Put the time prefix and time label into a QWidget
        time_widget = QWidget(self)
        time_layout = QHBoxLayout(time_widget)
        # time_layout.set
        time_layout.addWidget(self.time_prefix_label)
        time_layout.addWidget(self.time_label)
        time_layout.setContentsMargins(0, 0, 0, 0)
        time_layout.setSpacing(0)  # Adjust to reduce spacing

        # Create restaurant list title and set its style
        self.restaurant_title = QLabel("Restaurant List", self)
        self.restaurant_title.setAlignment(Qt.AlignLeft)

        # Set ObjectName
        self.restaurant_title.setObjectName("restaurant_title")

        # Use QHBoxLayout to display the time label and restaurant list title side by side
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.restaurant_title)
        title_layout.addStretch()
        title_layout.addWidget(time_widget)

        layout.addLayout(title_layout)

        # scroll area -> every element in area
        # Put the restaurant list into a scrollable container
        # laoding area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        # self.scroll_area.setLineWidth(3)
        self.scroll_area.setFrameStyle(QFrame.WinPanel | QFrame.Plain)
        layout.addWidget(self.scroll_area)

        # scroll content
        # the content in scroll area -> image, title, restaurant name
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_content)

        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignCenter)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)

        # Loading animation in the center of the scroll area
        self.loading_texts = [
            "▁氣集 ╰(〒皿〒)╯ 集氣 ▁", 
            "▂▁氣集 ╰(〒皿〒)╯ 集氣 ▁▂", 
            "▃▂▁氣集 ╰(〒皿〒)╯ 集氣 ▁▂▃", 
            "▄▃▂▁氣集 ╰(〒皿〒)╯ 集氣 ▁▂▃▄", 
            "▆▅▄▃▂▁氣集 ╰(〒皿〒)╯ 集氣 ▁▂▃▄▅▆", 
            "◢▆▅▄▃▂▁氣集 ╰(〒皿〒)╯ 集氣 ▁▂▃▄▅▆◣"
        ]
        self.loading_index = 0

        # the images were loaded
        self.loading_image_label = QLabel(self)
        self.loading_image_label.setAlignment(Qt.AlignCenter)
        self.scroll_layout.addWidget(self.loading_image_label)

        # the loading contents
        self.loading_label = QLabel(self.loading_texts[self.loading_index], self.scroll_content)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.scroll_layout.addWidget(self.loading_label)

        self.loading_image_timer = QTimer(self)
        self.loading_image_timer.timeout.connect(self.update_loading_image)
        self.loading_image_timer.start(250)

        # 在視窗最下方加入進度條
        self.pbar = CustomProgressBar()
        self.pbar.setTextVisible(False)  # 隱藏百分比顯示
        layout.addWidget(self.pbar)

        # 使用原有檔案的滾動條
        self.sbar = self.scroll_area.verticalScrollBar()
        self.sbar.setMaximum(100)  # 設置滾動條最大值
        self.sbar.valueChanged.connect(self.updateProgress)
        
        self.random_button = QPushButton("Random Recommendation", self)
        self.random_button.clicked.connect(self.show_random_recommendation)
        layout.addWidget(self.random_button)
        
        self.refresh_button = QPushButton("Refresh", self)
        self.refresh_button.clicked.connect(self.refresh_restaurants)
        layout.addWidget(self.refresh_button)

        self.button_layout = QVBoxLayout()
        self.close_button = QPushButton("Exit", self)
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button, alignment=Qt.AlignRight)
        layout.addLayout(self.button_layout)

        self.setLayout(layout)

        # loading restaurant list
        self.loader = RestaurantLoader()
        self.loader.restaurants_loaded.connect(self.show_restaurants)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_loading_text)
        self.timer.start(300)

        self.loader.start()

        # Start the time update timer
        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)  # Update time every second

        # Cursor position detection timer
        self.cursor_timer = QTimer(self)
        self.cursor_timer.timeout.connect(self.check_cursor_position)
        self.cursor_timer.start(100)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.time_label.setText(current_time)
        self.time_label.setStyleSheet("margin: 5px;")
        
    def update_loading_text(self):
        self.loading_label.setText(self.loading_texts[self.loading_index])
        self.loading_index = (self.loading_index + 1) % len(self.loading_texts)
    
    def update_loading_image(self):
        image_path = get_resource_path(f"UI/img/map_{self.loading_index}.png")
        pixmap = QPixmap(image_path)
        self.loading_image_label.setPixmap(pixmap)
        self.update_loading_text()

    def show_restaurants(self, restaurants):
        self.timer.stop()

        # Hide loading labels
        self.loading_label.hide()
        self.loading_image_label.hide()

        for restaurant in restaurants:
            restaurant_widget = self.create_restaurant_widget(restaurant)
            self.scroll_layout.addWidget(restaurant_widget)

        self.restaurants = restaurants
        self.scroll_area.setFrameStyle(QFrame.StyledPanel | QFrame.Plain) # 最外面的框框
        
    def updateProgress(self, value):
        if self.sbar.maximum() != 0:  # 檢查滾動條的最大值是否為 0
            
            value_normalized = self.sbar.value() / self.sbar.maximum()  # 使用滾動條的當前位置來計算進度
            self.pbar.setValue(int(value_normalized * 100))  # 將進度條的值設置為滾動條的當前位置的百分比

            # 計算漸變顏色
            gradient = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#4b0082", "#8a2be2"]
            value_normalized = value / self.sbar.maximum()
            color_index = int(value_normalized * (len(gradient) - 1))

            # 設置進度條樣式
            self.setProgressBarStyle(chunkBackgroundColor=gradient[color_index], borderRadius=10)


    def setProgressBarStyle(self, backgroundColor="#ffffff", chunkBackgroundColor="#00ff00", borderRadius=0):
        style = f"""
            QProgressBar {{
                border: 2px solid grey;
                border-radius: {borderRadius}px;
                background-color: {backgroundColor};  /* 設置未完成部分為白色 */
            }}
            QProgressBar::chunk {{
                background-color: {chunkBackgroundColor};
                border-radius: {borderRadius}px; /* 設置已完成部分為彩虹色 */
                margin-right: 1px;
            }}
        """
        self.pbar.setStyleSheet(style)

    def create_restaurant_widget(self, restaurant):
        '''
        The style of the scroll area.
        '''
        frame = QFrame(self.scroll_content)
        frame.setFrameShape(QFrame.StyledPanel | QFrame.Plain)
        frame.setFrameShadow(QFrame.Raised)
        frame.setStyleSheet("background-color: transparent; padding: 10px; margin-bottom: "
                            "10px;")
        frame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        frame.setObjectName("restaurant-widget")

        # shadow effect
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(4, 4)
        frame.setGraphicsEffect(shadow_effect)

        layout = QHBoxLayout(frame)

        icon_label = QLabel(frame)
        icon_label.setFixedSize(80, 80)
        restaurant_name = restaurant[0]

        if "麵" in restaurant_name:
            icon_path = get_resource_path("UI/img/icon/noodle_icon.png")
        elif "鍋" in restaurant_name:
            icon_path = get_resource_path("UI/img/icon/hotpot_icon.png")
        elif "果" in restaurant_name:
            icon_path = get_resource_path("UI/img/icon/fruit_icon.png")
        elif "甜" in restaurant_name or "豆" in restaurant_name:
            icon_path = get_resource_path("UI/img/icon/dessert_icon.png")
        elif "茶" in restaurant_name or "飲" in restaurant_name or "咖" in restaurant_name:
            icon_path = get_resource_path("UI/img/icon/tea_icon.png")
        elif "堡" in restaurant_name:
            icon_path = get_resource_path("UI/img/icon/Hamburger_icon.png")
        else:
            icon_path = get_resource_path("UI/img/icon/default_icon.png")

        pixmap = QPixmap(icon_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)

        name_label = QLabel(restaurant_name, frame)
        name_label.setStyleSheet("font-size: 20px; padding-left: 10px;")

        if len(restaurant_name) > 20:
            wrapped_name = "\n".join([restaurant_name[i:i+20] for i in range(0, len(restaurant_name), 20)])
            name_label.setText(wrapped_name)
        else:
            name_label.setText(restaurant_name)

        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        layout.addStretch()

        address_button = QPushButton("Address", frame)
        address_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(restaurant[1])))
        address_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.5); /* 半透明的白色背景 */
                color: #000000; /* 黑色文字 */
                border: none;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 18px;
                height: 22.5px; /* 高度縮小一半 */
                width: 100px;
                margin: 6px 3px;
                border-radius: 10px;    
            }
            QPushButton:hover {
                background-color: #F15B5D;
                border: 2px solid #EF8B70;
                color: #F5F5F9;
            }
        """)
        layout.addWidget(address_button)

        return frame

    def show_random_recommendation(self):
        if hasattr(self, 'restaurants') and self.restaurants:
            recommended = random.choice(self.restaurants)
            if not hasattr(self, 'recommendation_dialog') or self.recommendation_dialog is None:
                self.recommendation_dialog = RecommendationDialog(recommended, parent=self)
            else:
                self.recommendation_dialog.update_recommendation(recommended)
            self.recommendation_dialog.show()
            self.recommendation_dialog.raise_()
            self.recommendation_dialog.activateWindow()

    def set_background_image(self, image_path):
        background_image = QPixmap(image_path)
        background_label = QLabel(self)
        background_label.setPixmap(background_image)
        background_label.setGeometry(0, 0, self.width(), self.height())
        background_label.setScaledContents(True)
        self.setStyleSheet("#restaurant-widget { border: 2px solid black; }")

    def check_cursor_position(self):
        cursor_pos = self.mapFromGlobal(self.cursor().pos())
        if self.scroll_area.geometry().contains(cursor_pos):
            if cursor_pos.y() < self.scroll_area.height() * 0.25:
                self.scroll_area.verticalScrollBar().setValue(
                    self.scroll_area.verticalScrollBar().value() - 20)
            elif cursor_pos.y() > self.scroll_area.height() * 0.75:
                self.scroll_area.verticalScrollBar().setValue(
                    self.scroll_area.verticalScrollBar().value() + 20)
    
    def refresh_restaurants(self):
        # 清空原先滾動區域的餐廳列表的所有內容
        for i in reversed(range(self.scroll_layout.count())): 
            self.scroll_layout.itemAt(i).widget().setParent(None)

        # 重新顯示載入動畫
        self.scroll_layout.addWidget(self.loading_image_label)
        self.scroll_layout.addWidget(self.loading_label)
        self.loading_label.show()
        self.loading_image_label.show()

        # 將進度條的值設置為 0
        self.pbar.setValue(0)

        # 重新啟動餐廳爬蟲
        self.loader.start()


class CustomProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_label = QLabel(self)
        self.icon_label.setPixmap(QPixmap(get_resource_path('UI/img/icon/loading.png')))

    def paintEvent(self, event):
        super().paintEvent(event)
        value = self.value() / self.maximum()
        x = self.width() * value - self.icon_label.width() / 2
        y = (self.height() - self.icon_label.height()) / 2
        self.icon_label.move(int(round(x)), int(round(y)))

class RecommendationDialog(QDialog):
    '''
    Open Recommendation Dialog.
    '''
    def __init__(self, recommendation, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Random Recommendation")
        self.setFixedSize(360, 340)
        
        # Remove "?" 
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Set background image
        background_label = QLabel(self)
        pixmap = QPixmap(get_resource_path("UI/img/background3.png"))
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, 360, 340)
        background_label.setScaledContents(True)

        self.setWindowIcon(QIcon(get_resource_path("UI/img/icon/icon.png")))

        self.center()

        layout = QVBoxLayout()

        self.recommendation_label = QLabel("", self)
        self.recommendation_label.setAlignment(Qt.AlignCenter)
        self.recommendation_label.setStyleSheet("font-size: 16pt;")
        layout.addWidget(self.recommendation_label)

        self.address_button = QPushButton("Address", self)
        self.address_button.clicked.connect(lambda: self.open_url(self.recommendation[1]))
        layout.addWidget(self.address_button)

        self.recommendation_button = QPushButton("Recommend Again", self)
        self.recommendation_button.clicked.connect(self.recommend_again)
        layout.addWidget(self.recommendation_button)

        self.close_button = QPushButton("Close Window", self)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        self.update_recommendation(recommendation)

    def update_recommendation(self, recommendation):
        self.recommendation = recommendation
        self.recommendation_label.setText(f"{recommendation[0]}")

    def open_url(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def recommend_again(self):
        new_recommendation = random.choice(self.parent().restaurants)
        self.update_recommendation(new_recommendation)

    def showEvent(self, event):
        super().showEvent(event)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
