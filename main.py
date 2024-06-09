import os
import sys

from PyQt5.QtWidgets import QApplication

from UI import RestaurantRecommender


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create UI instance
    window = RestaurantRecommender()

    # Load stylesheet
    style_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "UI", "UI_style.qss"
    )
    with open(style_path, "r", encoding="utf-8") as f:
        app.setStyleSheet(f.read())

    # Show the UI
    window.show()

    sys.exit(app.exec_())
