"""MagicSquare_00 — PyQt6 최소 GUI 데모."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from entity.blank_loc import blank_coords_row_major
from entity.constants import BLANK, GRID_SIZE, MAGIC_CONSTANT
from entity.solver import solve_step_a
from validate_lines import validate_lines

SAMPLES: dict[str, list[list[int]]] = {
    "grid_g1 (빈칸 2)": [
        [1, 2, 3, 4],
        [5, 0, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 0, 16],
    ],
    "grid_complete (정답)": [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ],
    "grid_g4 (D2 오류)": [
        [1, 16, 16, 1],
        [16, 1, 1, 16],
        [16, 1, 16, 1],
        [1, 16, 1, 16],
    ],
}


def _format_cell(value: int) -> str:
    return "" if value == BLANK else str(value)


def _parse_cell(text: str) -> int:
    stripped = text.strip()
    if stripped in ("", "0"):
        return BLANK
    return int(stripped)


class MagicSquareWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MagicSquare_00 — 4×4 검증 데모")
        self.resize(520, 420)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        grid_box = QGroupBox("4×4 격자 (빈칸: 비우거나 0)")
        grid_layout = QGridLayout(grid_box)
        self._cells: list[list[QLineEdit]] = []
        for r in range(GRID_SIZE):
            row: list[QLineEdit] = []
            for c in range(GRID_SIZE):
                edit = QLineEdit()
                edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
                edit.setMaxLength(2)
                edit.setFixedWidth(48)
                grid_layout.addWidget(edit, r, c)
                row.append(edit)
            self._cells.append(row)
        layout.addWidget(grid_box)

        sample_row = QHBoxLayout()
        for name in SAMPLES:
            btn = QPushButton(name.split(" ")[0])
            btn.setToolTip(name)
            btn.clicked.connect(lambda _checked=False, n=name: self._load_sample(n))
            sample_row.addWidget(btn)
        layout.addLayout(sample_row)

        action_row = QHBoxLayout()
        validate_btn = QPushButton("10선 검증")
        validate_btn.clicked.connect(self._on_validate)
        action_row.addWidget(validate_btn)
        clear_btn = QPushButton("초기화")
        clear_btn.clicked.connect(self._on_clear)
        action_row.addWidget(clear_btn)
        layout.addLayout(action_row)

        self._status = QLabel("격자를 입력하거나 샘플을 불러온 뒤 「10선 검증」을 누르세요.")
        self._status.setWordWrap(True)
        layout.addWidget(self._status)

        self._detail = QLabel("")
        self._detail.setWordWrap(True)
        self._detail.setStyleSheet("color: #444;")
        layout.addWidget(self._detail)

        self._load_sample("grid_g1 (빈칸 2)")

    def _read_grid(self) -> list[list[int]]:
        grid: list[list[int]] = []
        for r in range(GRID_SIZE):
            row: list[int] = []
            for c in range(GRID_SIZE):
                row.append(_parse_cell(self._cells[r][c].text()))
            grid.append(row)
        return grid

    def _write_grid(self, grid: list[list[int]]) -> None:
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self._cells[r][c].setText(_format_cell(grid[r][c]))

    def _load_sample(self, name: str) -> None:
        self._write_grid(SAMPLES[name])
        self._status.setText(f"샘플 로드: {name}")
        self._detail.setText("")

    def _on_clear(self) -> None:
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self._cells[r][c].clear()
        self._status.setText("격자를 비웠습니다.")
        self._detail.setText("")

    def _on_validate(self) -> None:
        try:
            grid = self._read_grid()
        except ValueError:
            QMessageBox.warning(self, "입력 오류", "셀 값은 0~16 정수만 입력할 수 있습니다.")
            return

        result = validate_lines(grid)
        status = result["status"]
        failed = result["failed_lines"]

        status_ko = {"pass": "통과", "fail": "실패", "incomplete": "미완성"}[status]
        self._status.setText(f"status: {status} ({status_ko})")

        lines: list[str] = []
        if status == "incomplete":
            coords = blank_coords_row_major(grid)
            ok, missing = solve_step_a(grid)
            lines.append(f"빈칸 좌표 (0-index): {coords}")
            if ok:
                lines.append(f"빠진 숫자: {missing}")
        elif status == "fail":
            for item in failed:
                lines.append(f"  · {item['id']} 합 = {item['sum']} (기대 {MAGIC_CONSTANT})")
        else:
            lines.append(f"10선(R1~R4, C1~C4, D1, D2) 모두 합 {MAGIC_CONSTANT}")

        self._detail.setText("\n".join(lines))


def main() -> int:
    app = QApplication(sys.argv)
    window = MagicSquareWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
