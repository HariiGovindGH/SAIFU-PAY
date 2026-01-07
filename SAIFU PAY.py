from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QTableWidget, QTableWidgetItem, QMessageBox,
    QComboBox, QHeaderView, QHBoxLayout, QFormLayout, QDateEdit, QTimeEdit
)
from PyQt5.QtGui import QFont, QColor, QBrush, QIcon
from PyQt5.QtCore import Qt, QDate, QTime, QDateTime
import sys
import csv
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import ScalarFormatter

# --- Custom Matplotlib Widget for Dark Theme ---
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = plt.Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.fig.patch.set_facecolor('#1e1e1e')

class FinanceTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 1600, 900)
        self.setWindowTitle("SAIFU PAY")
        self.setFont(QFont("Segoe UI", 12))
        self.data_file = "finance_data.csv"
        
        # --- DEFINING CATEGORIES ---
        self.INCOME_CATEGORIES = ["Salary", "Investment", "Freelance", "Gift", "Refund", "Other Income"]
        self.EXPENSE_CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Education", "Other Expense"]

        try:
            self.setWindowIcon(QIcon(r"C:\Users\Harigovind\Downloads\wallet.ico"))
        except Exception as e:
            print(f"Could not load wallet.png icon: {e}")

        self.view_month_selector = QComboBox()
        self.stats_month_selector = QComboBox()

        self.init_ui()
        self.load_transactions()

    def apply_dark_modern_theme(self):
        self.setStyleSheet("""
            QWidget { background-color: #1e1e1e; color: white; font-family: Segoe UI; font-size: 16px; }
            QTabWidget::pane { border: 0; }
            QTabBar::tab { background: #333; padding: 12px 20px; margin-right: 2px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: #555; font-weight: bold; }
            QLineEdit, QComboBox, QDateEdit, QTimeEdit { background-color: #2d2d2d; padding: 8px; border: 1px solid #555; border-radius: 4px; color: white; }
            QTableWidget { background-color: #121212; gridline-color: #333; selection-background-color: #3d3d3d; }
            QHeaderView::section:horizontal { background-color: #121212; color: white; padding: 8px; border: 1px solid #333; font-weight: bold; }
            QHeaderView::section:vertical { background-color: #1e1e1e; color: white; border: 1px solid #333; }
            QTableWidget::item { background-color: #1e1e1e; color: white; padding: 5px; }
            QTableCornerButton::section { background-color: #1e1e1e; border: 1px solid #333; }
            QLabel { font-size: 18px; }
            
            /* Specific styling for QMessageBox included here to ensure global application */
            QMessageBox { background-color: #1e1e1e; }
            QMessageBox QLabel { color: white; }
        """)

    def style_button(self, btn, color="#555"):
        btn.setStyleSheet(f"""
            QPushButton {{ background-color: {color}; color: white; border-radius: 6px; padding: 10px; font-weight: bold; }}
            QPushButton:hover {{ filter: brightness(110%); background-color: {color}AA; }}
        """)

    def init_ui(self):
        self.apply_dark_modern_theme()
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.add_tab = QWidget()
        self.view_tab = QWidget()
        self.stats_tab = QWidget()

        self.tabs.addTab(self.add_tab, "➕ Add Transaction")
        self.tabs.addTab(self.view_tab, "📄 View Transactions")
        self.tabs.addTab(self.stats_tab, "📊 Statistics")

        self.tabs.currentChanged.connect(self.on_tab_change)

        self.setup_add_tab()
        self.setup_view_tab()
        self.setup_stats_tab()

        main_layout.addWidget(self.tabs)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def on_tab_change(self, index):
        self.populate_filter_combo_boxes()
        if index == 1: self.load_transactions()
        elif index == 2: self.generate_chart()

    def get_unique_filter_periods(self):
        periods = set()
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                for row in csv.reader(f):
                    if len(row) > 0 and row[0]:
                        try:
                            dt = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                            periods.add(dt.strftime("%Y-%m"))
                        except ValueError:
                            continue
        sorted_periods = sorted(list(periods), reverse=True)
        return ["All Periods"] + sorted_periods

    def create_filter_widget(self, cmb):
        h_layout = QHBoxLayout()
        lbl = QLabel("Filter By Year/Month:")
        h_layout.addWidget(lbl)
        h_layout.addWidget(cmb)
        return h_layout
    
    def populate_filter_combo_boxes(self):
        periods = self.get_unique_filter_periods()
        
        current_view_text = self.view_month_selector.currentText()
        current_stats_text = self.stats_month_selector.currentText()
        
        self.view_month_selector.blockSignals(True)
        self.stats_month_selector.blockSignals(True)
        
        self.view_month_selector.clear()
        self.stats_month_selector.clear()
        
        self.view_month_selector.addItems(periods)
        self.stats_month_selector.addItems(periods)
        
        view_index = self.view_month_selector.findText(current_view_text)
        if view_index >= 0:
            self.view_month_selector.setCurrentIndex(view_index)
        
        stats_index = self.stats_month_selector.findText(current_stats_text)
        if stats_index >= 0:
            self.stats_month_selector.setCurrentIndex(stats_index)
            
        self.view_month_selector.blockSignals(False)
        self.stats_month_selector.blockSignals(False)

    def reset_form(self):
        self.date_input.setDate(QDate.currentDate())
        self.time_input.setTime(QTime.currentTime())
        self.amount_input.clear()
        self.note_input.clear()

    # --- TAB 1: Add Transaction ---
    def setup_add_tab(self):
        layout = QVBoxLayout()
        title = QLabel("Add New Transaction")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        
        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        
        self.time_input = QTimeEdit(QTime.currentTime())
        self.time_input.setDisplayFormat("HH:mm")

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        
        # 1. Initialize Type Input FIRST
        self.type_input = QComboBox()
        self.type_input.addItems(["Expense", "Income"]) 
        
        # 2. Initialize Category Input
        self.category_input = QComboBox()
        
        # 3. Connect Type change to Category update
        self.type_input.currentIndexChanged.connect(self.update_categories)
        
        # 4. Trigger update immediately
        self.update_categories()

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Description...")
        
        btn_reset = QPushButton("Reset")
        self.style_button(btn_reset, "#778899")
        btn_reset.clicked.connect(self.reset_form)
        
        btn_add = QPushButton("Save Transaction")
        self.style_button(btn_add, "#2E7D32")
        btn_add.clicked.connect(self.save_transaction)

        date_time_reset_layout = QHBoxLayout()
        date_time_reset_layout.addWidget(self.date_input)
        date_time_reset_layout.addWidget(self.time_input)
        date_time_reset_layout.addWidget(btn_reset)
        date_time_reset_layout.addStretch()

        form_layout.addRow("Date/Time:", date_time_reset_layout)
        form_layout.addRow("Type:", self.type_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Amount (₹):", self.amount_input)
        form_layout.addRow("Note:", self.note_input)
        form_layout.addRow("", btn_add)
        
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        form_widget.setFixedWidth(550)
        
        layout.addWidget(form_widget, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        self.add_tab.setLayout(layout)
        self.populate_filter_combo_boxes()

    # --- Logic to update category dropdown ---
    def update_categories(self):
        selected_type = self.type_input.currentText()
        self.category_input.clear()
        
        if selected_type == "Income":
            self.category_input.addItems(self.INCOME_CATEGORIES)
        else:
            self.category_input.addItems(self.EXPENSE_CATEGORIES)

    # --- TAB 2: View Transactions ---
    def setup_view_tab(self):
        layout = QVBoxLayout()
        
        filter_layout = self.create_filter_widget(self.view_month_selector)
        
        btn_apply_filter = QPushButton("Apply Filter")
        self.style_button(btn_apply_filter, "#4682B4")
        btn_apply_filter.clicked.connect(self.load_transactions)
        
        self.view_month_selector.currentIndexChanged.connect(self.load_transactions)

        filter_layout.addWidget(btn_apply_filter)
        layout.addLayout(filter_layout)
        
        self.lbl_balance = QLabel("Net Balance: ₹0.00")
        self.lbl_balance.setAlignment(Qt.AlignCenter)
        self.lbl_balance.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.lbl_balance)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date/Time", "Amount", "Category", "Type", "Note"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setDefaultSectionSize(30)
        
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_del = QPushButton("Delete Selected")
        self.style_button(btn_del, "#C62828")
        btn_del.clicked.connect(self.delete_selected)
        
        btn_refresh = QPushButton("Refresh")
        self.style_button(btn_refresh, "#1565C0")
        btn_refresh.clicked.connect(self.load_transactions)
        
        btn_layout.addWidget(btn_del)
        btn_layout.addWidget(btn_refresh)
        layout.addLayout(btn_layout)

        self.view_tab.setLayout(layout)

    # --- TAB 3: Statistics ---
    def setup_stats_tab(self):
        layout = QVBoxLayout()
        
        controls = QHBoxLayout()
        filter_layout = self.create_filter_widget(self.stats_month_selector)
        controls.addLayout(filter_layout)
        
        btn_refresh_chart = QPushButton("Refresh Chart")
        self.style_button(btn_refresh_chart, "#1565C0")
        
        btn_refresh_chart.clicked.connect(self.generate_chart)
        self.stats_month_selector.currentIndexChanged.connect(self.generate_chart)
        
        self.chart_selector = QComboBox()
        self.chart_selector.addItems([
            "Dashboard (All Charts)", 
            "Pie: Total Income vs Expense", 
            "Pie: Expense Breakdown", 
            "Pie: Income Breakdown",
            "Bar: Category Breakdown" 
        ])
        self.chart_selector.currentIndexChanged.connect(self.generate_chart)

        controls.addWidget(self.chart_selector)
        controls.addWidget(btn_refresh_chart)
        layout.addLayout(controls)

        title = QLabel("Financial Analytics")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        
        self.stats_chart_canvas = MplCanvas(self, width=12, height=6)
        layout.addWidget(self.stats_chart_canvas)


        self.stats_tab.setLayout(layout)

    # --- Save Transaction with LARGE Success Box ---
    def save_transaction(self):
        amt = self.amount_input.text()
        cat = self.category_input.currentText()
        typ = self.type_input.currentText()
        note = self.note_input.text()

        try:
            val = float(amt)
            if val <= 0: raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid Amount")
            return

        final_amt = val if typ == "Income" else -val
        
        date_part = self.date_input.date()
        time_part = self.time_input.time()
        combined_datetime = QDateTime(date_part, time_part)
        
        selected_date_time = combined_datetime.toString("yyyy-MM-dd HH:mm:00")

        with open(self.data_file, 'a', newline='') as f:
            csv.writer(f).writerow([selected_date_time, f"{final_amt:.2f}", cat, typ, note])
        
        self.amount_input.clear()
        self.note_input.clear()
        
        # --- LARGE CUSTOM SUCCESS MESSAGE BOX ---
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Success")
        msg_box.setText("Transaction Saved Successfully!")
        msg_box.setIcon(QMessageBox.Information)
        
        # Apply style sheet specifically to this box
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e1e1e;
                min-width: 400px;
                min-height: 200px;
            }
            QLabel {
                color: white;
                font-size: 18px; 
                min-height: 60px;
                padding: 20px;
            }
            QPushButton {
                background-color: #2E7D32;
                color: white;
                padding: 8px 20px;
                font-size: 14px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        msg_box.exec_()
        # ----------------------------------------
        
        self.load_transactions()
        self.populate_filter_combo_boxes()

    def load_transactions(self):
        self.table.setRowCount(0)
        total = 0.0
        
        selected_period = self.view_month_selector.currentText()

        if not os.path.exists(self.data_file):
            self.lbl_balance.setText(f"Net Balance: ₹0.00")
            return

        with open(self.data_file, 'r') as f:
            rows = list(csv.reader(f))
            
            for row in rows:
                if len(row) < 5: continue 
                
                date_time_str = row[0] 
                match_period = (selected_period == "All Periods" or date_time_str.startswith(selected_period))
                
                if not match_period:
                    continue

                idx = self.table.rowCount()
                self.table.insertRow(idx)
                
                try: 
                    val = float(row[1])
                    total += val
                except: 
                    pass

                for i, d in enumerate(row):
                    item = QTableWidgetItem(d)
                    
                    if i == 3: # Type column
                        item.setForeground(QBrush(QColor("#66BB6A" if d == "Income" else "#EF5350")))
                    
                    if i == 1: # Amount column
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        
                    self.table.setItem(idx, i, item)

        self.lbl_balance.setText(f"Net Balance: ₹{total:,.2f}")
        color = "#66BB6A" if total >= 0 else "#EF5350"
        self.lbl_balance.setStyleSheet(f"font-size: 24px; font-weight: bold; margin: 10px; color: {color};")

    def generate_chart(self):
        self.stats_chart_canvas.fig.clear()
        
        selected_period = self.stats_month_selector.currentText()

        income_map = {}
        expense_map = {}
        total_inc = 0
        total_exp = 0

        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                for row in csv.reader(f):
                    if len(row) < 5: continue 
                    
                    date_time_str = row[0] 
                    match_period = (selected_period == "All Periods" or date_time_str.startswith(selected_period))
                    
                    if not match_period:
                        continue
                    
                    try:
                        amt = float(row[1])
                        cat = row[2]
                        typ = row[3]
                        
                        if typ == "Income":
                            total_inc += amt
                            income_map[cat] = income_map.get(cat, 0) + amt
                        else:
                            abs_amt = abs(amt)
                            total_exp += abs_amt
                            expense_map[cat] = expense_map.get(cat, 0) + abs_amt
                    except: continue

        mode = self.chart_selector.currentText()

        def draw_pie(ax, data_map, title, colors=None):
            ax.set_facecolor('#1e1e1e')
            filtered_data = {k: v for k, v in data_map.items() if v > 0}

            if not filtered_data:
                ax.text(0.5, 0.5, "No Data", ha='center', color='white', transform=ax.transAxes)
                ax.set_title(title, color='white', fontsize=14, fontweight='bold')
                return
            
            labels = list(filtered_data.keys())
            values = list(filtered_data.values())
            
            wedges, texts, autotexts = ax.pie(
                values, labels=labels, autopct='%1.1f%%', startangle=90, 
                colors=colors, wedgeprops={'edgecolor': '#1e1e1e', 'linewidth': 2}
            )
            for t in texts + autotexts: t.set_color('white')
            ax.set_title(title, color='white', fontsize=14, fontweight='bold')

        if mode == "Dashboard (All Charts)":
            ax1 = self.stats_chart_canvas.fig.add_subplot(131)
            ax2 = self.stats_chart_canvas.fig.add_subplot(132)
            ax3 = self.stats_chart_canvas.fig.add_subplot(133)
            
            draw_pie(ax1, {"Income": total_inc, "Expense": total_exp}, "Total Overview", ['#66BB6A', '#EF5350'])
            draw_pie(ax2, income_map, "Income Breakdown")
            draw_pie(ax3, expense_map, "Expense Breakdown")

        elif mode == "Pie: Total Income vs Expense":
            ax = self.stats_chart_canvas.fig.add_subplot(111)
            draw_pie(ax, {"Income": total_inc, "Expense": total_exp}, "Income vs Expense", ['#66BB6A', '#EF5350'])

        elif mode == "Pie: Income Breakdown":
            ax = self.stats_chart_canvas.fig.add_subplot(111)
            draw_pie(ax, income_map, "Income Sources Breakdown")

        elif mode == "Pie: Expense Breakdown":
            ax = self.stats_chart_canvas.fig.add_subplot(111)
            draw_pie(ax, expense_map, "Expense Category Breakdown")

        elif mode == "Bar: Category Breakdown": 
            ax = self.stats_chart_canvas.fig.add_subplot(111)
            ax.set_facecolor('#1e1e1e')
            
            all_cats = sorted(list(set(list(income_map.keys()) + list(expense_map.keys()))))
            
            if not all_cats:
                ax.text(0.5, 0.5, "No Data", ha='center', color='white', transform=ax.transAxes)
                ax.set_title("Income vs Expense by Category", color='white')
            else:
                inc_vals = [income_map.get(c, 0) for c in all_cats]
                exp_vals = [expense_map.get(c, 0) for c in all_cats]
                
                bar_width = 0.4
                x = range(len(all_cats))
                
                ax.bar([i - bar_width/2 for i in x], inc_vals, width=bar_width, label="Income", color="#66BB6A")
                ax.bar([i + bar_width/2 for i in x], exp_vals, width=bar_width, label="Expense", color="#EF5350")
                
                if max(inc_vals + exp_vals) > 0:
                    ax.set_ylim(0, max(max(inc_vals), max(exp_vals)) * 1.1)
                else:
                    ax.set_ylim(0, 10)
                
                formatter = ScalarFormatter(useOffset=False, useMathText=False)
                formatter.set_scientific(False)
                ax.yaxis.set_major_formatter(formatter)
                
                ax.set_xticks(list(x))
                ax.set_xticklabels(all_cats, rotation=30, ha='right') 
                ax.set_xlabel("Category", color='white')

                ax.set_ylabel("Amount (₹)", color='white') 
                
                ax.tick_params(axis='both', which='major', colors='white', labelcolor='white')
                
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.spines['right'].set_color('white')
                ax.spines['top'].set_color('white')
                
                ax.legend(facecolor='#333', labelcolor='white')
                ax.grid(axis='y', linestyle='--', alpha=0.3)
                ax.set_title("Income vs Expense by Category", color='white')

        self.stats_chart_canvas.fig.tight_layout()
        self.stats_chart_canvas.draw()
        
    def delete_selected(self):
        rows = sorted(set(idx.row() for idx in self.table.selectedIndexes()), reverse=True)
        if not rows: return
        if QMessageBox.question(self, "Confirm", "Delete selected?") != QMessageBox.Yes: return

        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                full_data = list(csv.reader(f))
            
            selected_period = self.view_month_selector.currentText()

            filtered_indices = []
            for i, row in enumerate(full_data):
                if len(row) < 5: continue
                date_time_str = row[0] 
                
                match_period = (selected_period == "All Periods" or date_time_str.startswith(selected_period))

                if match_period:
                    filtered_indices.append(i)
            
            indices_to_delete = {filtered_indices[r] for r in rows}
            
            new_data = [row for i, row in enumerate(full_data) if i not in indices_to_delete]

            with open(self.data_file, 'w', newline='') as f: csv.writer(f).writerows(new_data)
            
            self.populate_filter_combo_boxes()
            self.load_transactions()

if __name__ == '__main__':
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    window = FinanceTrackerApp()
    window.show()
    sys.exit(app.exec_())