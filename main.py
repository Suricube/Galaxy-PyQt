import sys
import asyncio
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
from qasync import QEventLoop, asyncSlot


class MainWindow(QMainWindow):
    def __init__(self, loop=None):
        super().__init__()
        button = QPushButton("Press This")
        self.setCentralWidget(button)
        button.clicked.connect(self.my_async_func)
        self.loop = loop or asyncio.get_event_loop()

    @asyncSlot()
    async def my_async_func(self):
        for x in range(1,10):
            print(x)
            await asyncio.sleep(1.0,self.loop)
        print("all done")


def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow(loop)
    window.show()
    
    with loop:
        loop.run_forever()


if __name__ == '__main__':
    main()