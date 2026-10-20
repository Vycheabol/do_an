
# Module này dùng để trực quan hóa kết quả thực nghiệm
# của hệ thống ẩn danh hóa dữ liệu.
#
# Dữ liệu đầu vào:
#
# 1. bang_xep_hang_candidate.csv
# 2. ket_qua_tong_hop_he_thong.csv
# Kết quả đầu ra:
# 1. Biểu đồ Suppression của các Candidate
# 2. Biểu đồ Data Retention của các Candidate
# 3. Biểu đồ Utility Score của các Candidate
# 4. Biểu đồ Selection Score của các Candidate
# 5. Biểu đồ so sánh Original và Anonymized trên Final Test


from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt



# 2. XÁC ĐỊNH THƯ MỤC PROJECT


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


# 3. XÁC ĐỊNH THƯ MỤC OUTPUT

OUTPUT_DIR = (
    PROJECT_ROOT
    / "outputs_bieu_do_ket_qua"
)


# Đảm bảo thư mục tồn tại.
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# 4. XÁC ĐỊNH CÁC FILE DỮ LIỆU ĐẦU VÀO

# File chứa bảng xếp hạng toàn bộ Candidate.
CANDIDATE_RANKING_FILE = (
    OUTPUT_DIR
    / "bang_xep_hang_candidate.csv"
)


# File chứa kết quả tổng hợp của Candidate thắng.
SYSTEM_SUMMARY_FILE = (
    OUTPUT_DIR
    / "ket_qua_tong_hop_he_thong.csv"
)


# 5. KIỂM TRA FILE ĐẦU VÀO

# Nếu chưa có bảng Candidate
# thì không thể vẽ biểu đồ.
if not CANDIDATE_RANKING_FILE.exists():

    raise FileNotFoundError(
        f"Không tìm thấy file: {CANDIDATE_RANKING_FILE}"
    )


# Nếu chưa có bảng tổng hợp
# thì không thể vẽ biểu đồ Final Test.
if not SYSTEM_SUMMARY_FILE.exists():

    raise FileNotFoundError(
        f"Không tìm thấy file: {SYSTEM_SUMMARY_FILE}"
    )


# 6. ĐỌC DỮ LIỆU

candidate_data = pd.read_csv(
    CANDIDATE_RANKING_FILE
)


summary_data = pd.read_csv(
    SYSTEM_SUMMARY_FILE
)


# 7. KIỂM TRA CÁC CỘT CẦN THIẾT

# Các cột bắt buộc trong bảng Candidate.
required_candidate_columns = [
    "rank",
    "strategy",
    "age_level",
    "hours_level",
    "privacy_valid",
    "suppression_percent",
    "data_retention_percent",
    "utility_score_percent",
    "selection_score",
    "eligible"
]


# Tìm các cột còn thiếu.
missing_candidate_columns = [
    column
    for column in required_candidate_columns
    if column not in candidate_data.columns
]


# Nếu thiếu thì dừng chương trình.
if missing_candidate_columns:

    raise ValueError(
        "Bảng Candidate thiếu các cột: "
        f"{missing_candidate_columns}"
    )

# 8. HÀM GHI GIÁ TRỊ TRÊN ĐẦU CỘT
def add_bar_labels(
    axis,
    bars
):
    """
    Hiển thị giá trị trên đầu mỗi cột của biểu đồ.
    """

    # Duyệt từng cột.
    for bar in bars:

        # Lấy chiều cao của cột.
        height = (
            bar.get_height()
        )


        # Ghi giá trị lên phía trên cột.
        axis.text(
            bar.get_x()
            +
            bar.get_width() / 2,

            height,

            f"{height:.2f}",

            ha="center",
            va="bottom",
            fontsize=9
        )

# 9. BIỂU ĐỒ 01 - SUPPRESSION

def create_suppression_chart():
    """
    So sánh tỷ lệ Suppression của các Candidate.
    """


    # Tạo Figure và Axis.
    figure, axis = plt.subplots(
        figsize=(9, 6)
    )


    # Vẽ biểu đồ cột.
    bars = axis.bar(
        candidate_data[
            "strategy"
        ],
        candidate_data[
            "suppression_percent"
        ]
    )


    # Tiêu đề biểu đồ.
    axis.set_title(
        "Tỷ lệ Suppression của các Candidate"
    )


    # Tên trục X.
    axis.set_xlabel(
        "Candidate"
    )


    # Tên trục Y.
    axis.set_ylabel(
        "Suppression (%)"
    )


    # Hiển thị giá trị trên cột.
    add_bar_labels(
        axis,
        bars
    )


    # Tự căn chỉnh bố cục.
    figure.tight_layout()


    # Đường dẫn file PNG.
    output_file = (
        OUTPUT_DIR
        / "bieu_do_01_suppression_candidate.png"
    )


    # Lưu biểu đồ.
    figure.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )


    # Đóng Figure để giải phóng bộ nhớ.
    plt.close(
        figure
    )


    return output_file


# 10. BIỂU ĐỒ 02 - DATA RETENTION
def create_data_retention_chart():
    """
    So sánh tỷ lệ dữ liệu được giữ lại
    sau quá trình ẩn danh hóa.
    """


    figure, axis = plt.subplots(
        figsize=(9, 6)
    )


    bars = axis.bar(
        candidate_data[
            "strategy"
        ],
        candidate_data[
            "data_retention_percent"
        ]
    )


    axis.set_title(
        "Tỷ lệ Data Retention của các Candidate"
    )


    axis.set_xlabel(
        "Candidate"
    )


    axis.set_ylabel(
        "Data Retention (%)"
    )


    # Vì các giá trị đều khá cao,
    # đặt giới hạn từ 0 đến 100
    # để biểu đồ phản ánh đúng tỷ lệ.
    axis.set_ylim(
        0,
        100
    )


    add_bar_labels(
        axis,
        bars
    )


    figure.tight_layout()


    output_file = (
        OUTPUT_DIR
        / "bieu_do_02_data_retention_candidate.png"
    )


    figure.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )


    plt.close(
        figure
    )


    return output_file

# 11. BIỂU ĐỒ 03 - UTILITY SCORE

def create_utility_chart():
    """
    So sánh Utility Score trên tập Validation
    của các Candidate.
    """


    figure, axis = plt.subplots(
        figsize=(9, 6)
    )


    bars = axis.bar(
        candidate_data[
            "strategy"
        ],
        candidate_data[
            "utility_score_percent"
        ]
    )


    axis.set_title(
        "Utility Score của các Candidate"
    )


    axis.set_xlabel(
        "Candidate"
    )


    axis.set_ylabel(
        "Utility Score (%)"
    )


    axis.set_ylim(
        0,
        100
    )


    add_bar_labels(
        axis,
        bars
    )


    figure.tight_layout()


    output_file = (
        OUTPUT_DIR
        / "bieu_do_03_utility_candidate.png"
    )


    figure.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )


    plt.close(
        figure
    )


    return output_file


# 12. BIỂU ĐỒ 04 - SELECTION SCORE

def create_selection_score_chart():
    """
    So sánh Selection Score của các Candidate.
    """


    figure, axis = plt.subplots(
        figsize=(9, 6)
    )


    bars = axis.bar(
        candidate_data[
            "strategy"
        ],
        candidate_data[
            "selection_score"
        ]
    )


    axis.set_title(
        "Selection Score của các Candidate"
    )


    axis.set_xlabel(
        "Candidate"
    )


    axis.set_ylabel(
        "Selection Score"
    )


    axis.set_ylim(
        0,
        100
    )


    add_bar_labels(
        axis,
        bars
    )


    figure.tight_layout()


    output_file = (
        OUTPUT_DIR
        / "bieu_do_04_selection_score_candidate.png"
    )


    figure.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )


    plt.close(
        figure
    )


    return output_file

# 13. BIỂU ĐỒ 05 - ORIGINAL VS ANONYMIZED
def create_original_vs_anonymized_chart():
    """
    So sánh chất lượng Machine Learning
    giữa dữ liệu Original và Anonymized
    trên tập Final Test.
    """


    # Vì bảng summary chỉ có một dòng,
    # lấy dòng đầu tiên.
    summary_row = (
        summary_data.iloc[
            0
        ]
    )

    # 13.1. TÊN CÁC METRIC

    metric_names = [
        "Accuracy",
        "F1 Score",
        "Balanced Accuracy",
        "ROC-AUC"
    ]

    # 13.2. METRIC ORIGINAL
    original_values = [
        summary_row[
            "original_test_accuracy_percent"
        ],

        summary_row[
            "original_test_f1_percent"
        ],

        summary_row[
            "original_test_balanced_accuracy_percent"
        ],

        summary_row[
            "original_test_roc_auc_percent"
        ]
    ]

    # 13.3. METRIC ANONYMIZED
    anonymized_values = [
        summary_row[
            "anonymized_test_accuracy_percent"
        ],

        summary_row[
            "anonymized_test_f1_percent"
        ],

        summary_row[
            "anonymized_test_balanced_accuracy_percent"
        ],

        summary_row[
            "anonymized_test_roc_auc_percent"
        ]
    ]

    # 13.4. VỊ TRÍ CÁC CỘT
    x_positions = list(
        range(
            len(
                metric_names
            )
        )
    )


    # Độ rộng mỗi cột.
    bar_width = 0.35

    # 13.5. TẠO BIỂU ĐỒ

    figure, axis = plt.subplots(
        figsize=(10, 6)
    )


    # Cột Original nằm lệch sang trái.
    original_bars = axis.bar(
        [
            position
            -
            bar_width / 2
            for position in x_positions
        ],
        original_values,
        width=bar_width,
        label="Original"
    )


    # Cột Anonymized nằm lệch sang phải.
    anonymized_bars = axis.bar(
        [
            position
            +
            bar_width / 2
            for position in x_positions
        ],
        anonymized_values,
        width=bar_width,
        label="Anonymized"
    )

    # 13.6. ĐỊNH DẠNG BIỂU ĐỒ
    axis.set_title(
        "So sánh Machine Learning trước và sau ẩn danh hóa"
    )


    axis.set_xlabel(
        "Metric"
    )


    axis.set_ylabel(
        "Score (%)"
    )


    axis.set_xticks(
        x_positions
    )


    axis.set_xticklabels(
        metric_names
    )


    axis.set_ylim(
        0,
        100
    )


    # Hiển thị chú thích Original / Anonymized.
    axis.legend()


    # Hiển thị số liệu trên từng cột.
    add_bar_labels(
        axis,
        original_bars
    )


    add_bar_labels(
        axis,
        anonymized_bars
    )


    figure.tight_layout()


    output_file = (
        OUTPUT_DIR
        / "bieu_do_05_original_vs_anonymized.png"
    )


    figure.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )


    plt.close(
        figure
    )


    return output_file

# 13.9. BIỂU ĐỒ 06 - SENSITIVITY ANALYSIS CHO TRỌNG SỐ
# File này do pipeline.py xuất ra ở bước Sensitivity Analysis.
SENSITIVITY_FILE = (
    OUTPUT_DIR
    / "sensitivity_analysis_trong_so.csv"
)


def create_sensitivity_chart():
    """
    Vẽ biểu đồ đường thể hiện Selection Score của từng Candidate
    thay đổi thế nào khi trọng số (Data Retention / Utility) thay đổi.

    Mục đích: cho thấy trực quan Candidate nào luôn đứng đầu/luôn đứng cuối
    dù đổi trọng số, và Candidate nào bị ảnh hưởng bởi cách chọn trọng số.

    Nếu chưa chạy pipeline.py (chưa có file sensitivity_analysis_trong_so.csv)
    thì hàm này sẽ báo lỗi rõ ràng thay vì crash khó hiểu.
    """

    if not SENSITIVITY_FILE.exists():

        raise FileNotFoundError(
            f"Không tìm thấy file: {SENSITIVITY_FILE}. "
            "Hãy chạy pipeline.py trước để tạo Sensitivity Analysis."
        )


    sensitivity_data = pd.read_csv(
        SENSITIVITY_FILE
    )


    # --------------------------------------------------------
    # 13.9.1. TRỤC X: TỶ LỆ TRỌNG SỐ DATA RETENTION
    # --------------------------------------------------------

    # Mỗi bộ trọng số được biểu diễn bằng % Data Retention
    # (utility_percent = 100 - data_retention_percent nên chỉ cần 1 trục).
    weight_labels = sorted(
        sensitivity_data[
            "weight_data_retention_percent"
        ].unique()
    )

    # 13.9.2. TẠO BIỂU ĐỒ
    figure, axis = plt.subplots(
        figsize=(10, 6)
    )


    # Vẽ một đường riêng cho từng Candidate.
    for strategy_name in sorted(
        sensitivity_data["strategy"].unique()
    ):

        strategy_rows = (
            sensitivity_data[
                sensitivity_data["strategy"] == strategy_name
            ]
            .sort_values(
                "weight_data_retention_percent"
            )
        )

        axis.plot(
            strategy_rows["weight_data_retention_percent"],
            strategy_rows["selection_score"],
            marker="o",
            label=strategy_name
        )


    axis.set_xlabel(
        "Trọng số Data Retention (%)  "
        "[Utility = 100 - giá trị này]"
    )

    axis.set_ylabel(
        "Selection Score"
    )

    axis.set_title(
        "Sensitivity Analysis: Selection Score theo trọng số"
    )

    axis.set_xticks(
        weight_labels
    )

    axis.legend()

    axis.grid(
        True,
        linestyle="--",
        alpha=0.4
    )


    figure.tight_layout()


    output_file = (
        OUTPUT_DIR
        / "bieu_do_06_sensitivity_analysis.png"
    )


    figure.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )


    plt.close(
        figure
    )


    return output_file

# 14. CHẠY TOÀN BỘ QUÁ TRÌNH VẼ BIỂU ĐỒ
def create_all_charts():
    """
    Tạo toàn bộ biểu đồ thực nghiệm.
    """


    # Danh sách dùng để lưu
    # đường dẫn các hình vừa tạo.
    created_files = []


    # Tạo biểu đồ Suppression.
    created_files.append(
        create_suppression_chart()
    )


    # Tạo biểu đồ Data Retention.
    created_files.append(
        create_data_retention_chart()
    )


    # Tạo biểu đồ Utility.
    created_files.append(
        create_utility_chart()
    )


    # Tạo biểu đồ Selection Score.
    created_files.append(
        create_selection_score_chart()
    )


    # Tạo biểu đồ so sánh ML.
    created_files.append(
        create_original_vs_anonymized_chart()
    )


    # Tạo biểu đồ Sensitivity Analysis cho trọng số Selection Score.
    if SENSITIVITY_FILE.exists():

        created_files.append(
            create_sensitivity_chart()
        )


    # Trả danh sách file vừa tạo.
    return created_files

# 15. CHẠY FILE TRỰC TIẾP
if __name__ == "__main__":

    # HIỂN THỊ THÔNG TIN ĐẦU VÀO

    print(
        "===== RESULT VISUALIZER ====="
    )


    print(
        "Project root:",
        PROJECT_ROOT
    )


    print(
        "Candidate ranking:",
        CANDIDATE_RANKING_FILE
    )


    print(
        "System summary:",
        SYSTEM_SUMMARY_FILE
    )


    print(
        "Số Candidate:",
        len(
            candidate_data
        )
    )


    # TẠO BIỂU ĐỒ

    created_chart_files = (
        create_all_charts()
    )


    print(
        "\nCÁC BIỂU ĐỒ ĐÃ TẠO "
    )


    for chart_file in created_chart_files:

        print(
            chart_file
        )


    # THÔNG BÁO HOÀN THÀNH

    print(
        "\nTổng số biểu đồ:",
        len(
            created_chart_files
        )
    )


    print(
        "Result Visualizer: THÀNH CÔNG"
    )