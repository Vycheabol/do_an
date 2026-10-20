
# Chứa các hàm dùng để đánh giá độ hữu ích của dữ liệu
# thông qua kết quả của mô hình Machine Learning.

# Import Accuracy để đo tỷ lệ dự đoán đúng trên toàn bộ dữ liệu.
from sklearn.metrics import accuracy_score

# Import Precision để đo độ chính xác khi mô hình dự đoán lớp >50K.
from sklearn.metrics import precision_score

# Import Recall để đo khả năng tìm đúng những người thực sự thuộc lớp >50K.
from sklearn.metrics import recall_score

# Import F1-score để cân bằng giữa Precision và Recall.
from sklearn.metrics import f1_score

# Import Balanced Accuracy để đánh giá cân bằng giữa hai lớp thu nhập.
from sklearn.metrics import balanced_accuracy_score

# Import ROC-AUC để đo khả năng phân biệt giữa <=50K và >50K.
from sklearn.metrics import roc_auc_score


# 1. HÀM ĐÁNH GIÁ KẾT QUẢ MÔ HÌNH MACHINE LEARNING


# Hàm evaluate_classification_metrics() dùng để tính
# 6 chỉ số đánh giá mô hình Machine Learning.#
def evaluate_classification_metrics(
    y_true,
    y_pred,
    y_prob,
    positive_label=">50K"
):

    # 1.1. ACCURACY
    # Accuracy cho biết tỷ lệ dự đoán đúng
    # trên toàn bộ dữ liệu.
    accuracy = accuracy_score(
        y_true,
        y_pred
    )


    # 1.2. PRECISION

    # Precision cho lớp >50K.
    #
    # Ví dụ:
    # Precision = 0.68
    #
    # nghĩa là trong những bản ghi được mô hình
    # dự đoán là >50K thì khoảng 68% thực sự đúng.
    precision = precision_score(
        y_true,
        y_pred,
        pos_label=positive_label
    )


    # 1.3. RECALL

    # Recall cho lớp >50K.
    #
    # Ví dụ:
    # Recall = 0.49
    #
    # nghĩa là trong tất cả những người thực sự >50K,
    # mô hình tìm đúng khoảng 49%.
    recall = recall_score(
        y_true,
        y_pred,
        pos_label=positive_label
    )


    # 1.4. F1-SCORE

    # F1-score là trung bình điều hòa
    # giữa Precision và Recall.
    #
    # Chỉ số này hữu ích khi cần cân bằng
    # giữa hai mục tiêu trên.
    f1 = f1_score(
        y_true,
        y_pred,
        pos_label=positive_label
    )


    # 1.5. BALANCED ACCURACY

    # Balanced Accuracy phù hợp khi hai lớp
    # <=50K và >50K không cân bằng về số lượng.
    balanced_accuracy = balanced_accuracy_score(
        y_true,
        y_pred
    )


    # 1.6. ROC-AUC

    # Chuyển nhãn thật thành dạng số:
    #
    # >50K  -> 1
    # <=50K -> 0
    #
    # ROC-AUC cần nhãn dạng nhị phân
    # để so sánh với xác suất dự đoán.
    y_true_binary = (
        (y_true == positive_label)
        .astype(int)
    )


    # ROC-AUC đo khả năng mô hình
    # phân biệt giữa hai lớp thu nhập.
    #
    # Giá trị càng gần 1 thì khả năng
    # phân biệt hai lớp càng tốt.
    roc_auc = roc_auc_score(
        y_true_binary,
        y_prob
    )


    # 1.7. TRẢ KẾT QUẢ
    # Trả về dictionary để các module khác
    # như ml_evaluator.py có thể sử dụng.
    return {

        # Accuracy của mô hình.
        "accuracy": accuracy,

        # Precision của lớp >50K.
        "precision": precision,

        # Recall của lớp >50K.
        "recall": recall,

        # F1-score của lớp >50K.
        "f1_score": f1,

        # Balanced Accuracy.
        "balanced_accuracy": balanced_accuracy,

        # ROC-AUC.
        "roc_auc": roc_auc
    }


# 2. HÀM TÍNH UTILITY RETENTION


# Hàm calculate_utility_retention() dùng để so sánh
# hiệu năng Machine Learning trước và sau khi ẩn danh.
# original_metrics:
#     Dictionary chứa metric của dữ liệu gốc.
#
# anonymized_metrics:
#     Dictionary chứa metric của dữ liệu đã ẩn danh.
def calculate_utility_retention(
    original_metrics,
    anonymized_metrics
):

    # 2.1. HÀM NỘI BỘ TÍNH RETENTION CHO MỘT METRIC

    # Hàm này được tạo để tránh lặp lại
    # cùng một công thức cho:
    #
    # - Accuracy
    # - F1
    # - Balanced Accuracy
    # - ROC-AUC
    def calculate_single_retention(
        original_value,
        anonymized_value
    ):

        # KIỂM TRA GIÁ TRỊ ĐẦU VÀO

        # Các metric classification bình thường
        # phải nằm trong khoảng từ 0 đến 1.
        #
        # Nếu nhận giá trị âm thì đây là dữ liệu
        # không hợp lệ đối với các metric đang sử dụng.
        if original_value < 0:

            raise ValueError(
                "Original metric không được nhỏ hơn 0."
            )


        if anonymized_value < 0:

            raise ValueError(
                "Anonymized metric không được nhỏ hơn 0."
            )


        # TRƯỜNG HỢP ORIGINAL = 0

        # Không thể thực hiện:
        #
        # anonymized / original
        #
        # nếu original bằng 0.
        #
        # Với dataset hiện tại trường hợp này
        # gần như không xảy ra, nhưng vẫn cần
        # xử lý để code an toàn.
        if original_value == 0:

            # Nếu cả hai cùng bằng 0,
            # ta coi mức bảo toàn là 100%
            # vì metric không bị suy giảm.
            if anonymized_value == 0:

                return 100.0


            # Nếu Original = 0 nhưng Anonymized > 0,
            # dữ liệu ẩn danh đang có kết quả tốt hơn.
            #
            # Vì Utility Retention bị giới hạn tối đa 100%,
            # nên trả về 100%.
            return 100.0


        # TÍNH RAW RETENTION

        # Công thức:
        #
        # Retention
        # =
        # Anonymized metric
        # /
        # Original metric
        # × 100
        raw_retention = (
            anonymized_value
            /
            original_value
            *
            100
        )


        # GIỚI HẠN RETENTION TRONG KHOẢNG 0 - 100

        # max(raw_retention, 0.0):
        # không cho retention nhỏ hơn 0%.
        #
        # min(..., 100.0):
        # không cho retention vượt quá 100%.
        #
        # Nhờ vậy:
        #
        # 0 <= retention <= 100
        retention = min(
            max(
                raw_retention,
                0.0
            ),
            100.0
        )


        # Trả retention chưa làm tròn.
        #
        # Chỉ làm tròn ở bước cuối,
        # tránh sai số khi tính Utility Score trung bình.
        return retention


    # 2.2. ACCURACY RETENTION

    # So sánh Accuracy của dữ liệu ẩn danh
    # với Accuracy của dữ liệu gốc.
    accuracy_retention = (
        calculate_single_retention(
            original_metrics[
                "accuracy"
            ],
            anonymized_metrics[
                "accuracy"
            ]
        )
    )


    # 2.3. F1-SCORE RETENTION

    # So sánh F1-score trước và sau ẩn danh.
    #
    # F1 là một trong 4 metric được sử dụng
    # để tính Utility Score tổng.
    f1_retention = (
        calculate_single_retention(
            original_metrics[
                "f1_score"
            ],
            anonymized_metrics[
                "f1_score"
            ]
        )
    )


    # 2.4. BALANCED ACCURACY RETENTION

    # So sánh Balanced Accuracy
    # trước và sau ẩn danh.
    balanced_accuracy_retention = (
        calculate_single_retention(
            original_metrics[
                "balanced_accuracy"
            ],
            anonymized_metrics[
                "balanced_accuracy"
            ]
        )
    )


    # 2.5. ROC-AUC RETENTION

    # So sánh khả năng phân biệt hai lớp
    # của mô hình trước và sau ẩn danh.
    roc_auc_retention = (
        calculate_single_retention(
            original_metrics[
                "roc_auc"
            ],
            anonymized_metrics[
                "roc_auc"
            ]
        )
    )


    # 2.6. TÍNH UTILITY SCORE TỔNG


    utility_score = (
        accuracy_retention
        +
        f1_retention
        +
        balanced_accuracy_retention
        +
        roc_auc_retention
    ) / 4


    # 2.7. TRẢ KẾT QUẢ UTILITY

    # Làm tròn chỉ khi trả kết quả.
    # Điều này giúp phép tính Utility Score phía trên
    # sử dụng giá trị chính xác hơn.
    return {

        # Tỷ lệ bảo toàn Accuracy.
        "accuracy_retention_%": round(
            accuracy_retention,
            2
        ),

        # Tỷ lệ bảo toàn F1-score.
        "f1_retention_%": round(
            f1_retention,
            2
        ),

        # Tỷ lệ bảo toàn Balanced Accuracy.
        "balanced_accuracy_retention_%": round(
            balanced_accuracy_retention,
            2
        ),

        # Tỷ lệ bảo toàn ROC-AUC.
        "roc_auc_retention_%": round(
            roc_auc_retention,
            2
        ),

        # Utility Score tổng hợp.
        #
        # Đây là Utility Score được sử dụng
        # trong quá trình Ranking Candidate.
        "utility_score_%": round(
            utility_score,
            2
        )
    }
