
# 1. Đọc dữ liệu gốc
# 2. Chạy các chiến lược ẩn danh hóa
# 3. Đánh giá mức độ bảo vệ Privacy
# 4. Đánh giá khả năng giữ lại Utility bằng Machine Learning
# 5. So sánh và xếp hạng các Strategy
# 6. Chọn Strategy tốt nhất
# 7. Đánh giá Strategy được chọn trên tập Test cuối cùng
# 8. Xuất dữ liệu ẩn danh ra file
#
# Hiện tại pipeline đã được chuyển sang cơ chế Candidate Strategy tự sinh,
# sau đó tự đánh giá Privacy, Utility, xếp hạng, chọn phương án tốt nhất,
# Final Test và xuất dữ liệu/kết quả tổng hợp.


from pathlib import Path


import sys

import pandas as pd


# 2. XÁC ĐỊNH THƯ MỤC GỐC CỦA PROJECT



PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
)


# 3. XÁC ĐỊNH THƯ MỤC src
SRC_DIR = (
    PROJECT_ROOT
    / "src"
)


# 4. THÊM src VÀO ĐƯỜNG DẪN TÌM KIẾM MODULE

# Bình thường Python chỉ import được module
# ở những thư mục mà nó biết.
#
# Vì các module của đồ án nằm trong src,
# ta phải thêm src vào sys.path.
#
# Kiểm tra trước để tránh thêm trùng nhiều lần.
if str(SRC_DIR) not in sys.path:

    # Chèn src vào vị trí đầu tiên trong sys.path.
    #
    # Sau bước này Python có thể import:
    # import anonymization_engine
    # import privacy_analyzer
    # ...
    sys.path.insert(
        0,
        str(SRC_DIR)
    )


# 5. IMPORT CÁC MODULE DO ĐỒ ÁN XÂY DỰNG

# anonymization_engine:
# chịu trách nhiệm thực hiện Generalization và Suppression,
# tức là biến dữ liệu gốc thành dữ liệu đã được ẩn danh.
import anonymization_engine


# privacy_analyzer:
# dùng để đánh giá Privacy,
# bao gồm k-anonymity và l-diversity.
import privacy_analyzer


# ml_evaluator:
# dùng để huấn luyện và đánh giá mô hình Machine Learning
import ml_evaluator


# utility_evaluator:
# dùng để tính Utility Retention,
import utility_evaluator


# strategy_selector:
# dùng để tính Selection Score,
# xếp hạng các Strategy
# và chọn Strategy tốt nhất.
import strategy_selector


# strategy_generator:
# tự động sinh các Candidate Strategy
# dựa trên những mức Generalization mà hệ thống hỗ trợ.
import strategy_generator


# 6. XÁC ĐỊNH ĐƯỜNG DẪN DATASET GỐC
DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "dataset_anonymization.csv"
)


# 7. KIỂM TRA MÔI TRƯỜNG PIPELINE

print(
    "===== KIỂM TRA PIPELINE ====="
)


# Hiển thị thư mục gốc của project
# để chắc chắn Python đang chạy đúng project.
print(
    "Project root:",
    PROJECT_ROOT
)


# Hiển thị vị trí thư mục src.
print(
    "Thư mục src:",
    SRC_DIR
)


# Hiển thị đường dẫn Dataset.
print(
    "Dataset:",
    DATA_FILE
)



print(
    "Dataset tồn tại?:",
    DATA_FILE.exists()
)


# Nếu chương trình chạy được đến đây
# nghĩa là các module phía trên đã import thành công.
print(
    "Import các module: THÀNH CÔNG"
)


# 8. ĐỌC DATASET GỐC


if not DATA_FILE.exists():

    # Nếu file không tồn tại,
    # dừng pipeline ngay và báo lỗi rõ ràng.
    #
    # Làm như vậy tốt hơn việc để pandas báo lỗi khó hiểu phía sau.
    raise FileNotFoundError(
        f"Không tìm thấy dataset tại: {DATA_FILE}"
    )


data = pd.read_csv(
    DATA_FILE
)


# 9. KIỂM TRA DATASET SAU KHI ĐỌC

# In tiêu đề để dễ đọc Console.
print(
    "\n===== ĐỌC DATASET GỐC ====="
)


# data.shape trả về:
# (số dòng, số cột)
#
# Kỳ vọng:
# (32561, 15)
print(
    "Kích thước dataset:",
    data.shape
)


# len(data) trả về tổng số dòng.
#
# Mỗi dòng tương ứng với một bản ghi.
print(
    "Số bản ghi:",
    len(
        data
    )
)


# data.columns chứa danh sách tên các cột.
#
# len(data.columns)
# → đếm tổng số cột.
print(
    "Số cột:",
    len(
        data.columns
    )
)


# Hiển thị tiêu đề trước khi in danh sách cột.
print(
    "Các cột:"
)


# Chuyển Index chứa tên cột thành list
# để kết quả dễ đọc hơn.
print(
    data.columns.tolist()
)


# Kiểm tra dataset có cột target "thu_nhap" hay không.
#
# Đây là biến mục tiêu mà Machine Learning
# sẽ dự đoán ở các bước sau.
print(
    "Có cột target thu_nhap?:",
    "thu_nhap"
    in data.columns
)


# Nếu không tồn tại cột thu_nhap,
# pipeline ML phía sau sẽ không thể chạy.
if "thu_nhap" not in data.columns:

    # Dừng chương trình và báo rõ nguyên nhân.
    raise ValueError(
        "Dataset không có cột target 'thu_nhap'."
    )

# 10. TỰ ĐỘNG SINH CÁC CANDIDATE STRATEGY

# Thay vì viết cứng strategy_1 và strategy_2,
# pipeline sẽ yêu cầu strategy_generator
# tự động tạo danh sách Candidate từ các mức Generalization hiện có.
candidate_strategies = (
    strategy_generator
    .generate_candidate_strategies()
)


# Kiểm tra toàn bộ Candidate vừa sinh có hợp lệ hay không.
candidate_strategies_valid = (
    strategy_generator
    .validate_candidate_strategies(
        candidate_strategies
    )
)


# Nếu danh sách Candidate không hợp lệ
# thì dừng pipeline ngay để tránh chạy sai cấu hình.
if not candidate_strategies_valid:

    raise ValueError(
        "Danh sách Candidate Strategy không hợp lệ."
    )

# 10.1. TẠO DICTIONARY TRA CỨU CANDIDATE THEO TÊN

# Dictionary này giúp pipeline lấy nhanh cấu hình Candidate theo tên.
strategy_configs = {

    # Dùng strategy_name của Candidate làm key.
    candidate[
        "strategy_name"
    ]:
        candidate

    # Duyệt toàn bộ Candidate vừa được sinh tự động.
    for candidate in candidate_strategies
}

# 10.2. TẠO DANH SÁCH TÊN CANDIDATE
# Các bước phía sau của pipeline đang sử dụng biến strategy_names.
# Ta giữ tên biến này để không phải sửa toàn bộ pipeline,
# nhưng nội dung của nó bây giờ được tạo tự động từ Candidate.
strategy_names = list(
    strategy_configs.keys()
)


# 10.3. TẠO NƠI LƯU KẾT QUẢ

# Dictionary này dùng để lưu toàn bộ kết quả
# của từng Candidate trong suốt pipeline.
strategy_results = {}

# 10.4. HIỂN THỊ CANDIDATE ĐƯỢC SINH TỰ ĐỘNG

print(
    "\n===== CANDIDATE STRATEGY ĐƯỢC SINH TỰ ĐỘNG ====="
)


print(
    "Số Candidate:",
    len(
        candidate_strategies
    )
)


# Hiển thị từng cấu hình Candidate để dễ kiểm tra trên Console.
for candidate in candidate_strategies:

    print(
        candidate
    )


# 11. TỰ ĐỘNG CHẠY TẤT CẢ CANDIDATE STRATEGY

# In tiêu đề trên Console.
print(
    "\n===== CHẠY CÁC CANDIDATE ẨN DANH ====="
)


#
for strategy_name in strategy_names:

    # Hiển thị Strategy đang chạy
    # để dễ theo dõi trên Console.
    print(
        "\nStrategy:",
        strategy_name
    )


    # 11.1. LẤY CẤU HÌNH VÀ CHẠY CANDIDATE

    # Lấy cấu hình của Candidate hiện tại.
    #
    # Ví dụ candidate_1 có thể có cấu hình:
    # {
    #     "strategy_name": "candidate_1",
    #     "age_level": "age3"
    # }
    strategy_config = (
        strategy_configs[
            strategy_name
        ]
    )


    # Chạy toàn bộ quá trình ẩn danh hóa theo cấu hình Candidate.
    #
    # Engine sẽ tự thực hiện:
    # Generalization
    #     ↓
    # k-anonymity Suppression
    #     ↓
    # l-diversity Suppression
    #     ↓
    # Release Data
    release_data, retained_indices = (
        anonymization_engine
        .anonymize_candidate_strategy(

            # Dataset gốc.
            dataframe=data,

            # Cấu hình Candidate hiện tại.
            strategy_config=strategy_config,

            # Ngưỡng k thực nghiệm của đồ án.
            # Đây không phải ngưỡng bắt buộc của GDPR.
            k_required=5,

            # Ngưỡng l thực nghiệm của đồ án.
            l_required=2
        )
    )


    # 11.2. TÍNH SỐ LƯỢNG BẢN GHI

    # Đếm tổng số bản ghi của dataset gốc.
    #
    # Với dataset hiện tại:
    # original_records = 32561
    original_records = len(
        data
    )


    # Đếm số bản ghi còn lại
    # sau khi Strategy đã Generalization + Suppression.
    released_records = len(
        release_data
    )


    # Tính số bản ghi đã bị loại bỏ.
    #
    # Công thức:
    #
    # Suppressed
    # = dữ liệu ban đầu - dữ liệu còn lại
    suppressed_records = (
        original_records
        -
        released_records
    )


    # 11.3. TÍNH TỶ LỆ SUPPRESSION

    # Suppression Percent cho biết
    # bao nhiêu phần trăm dữ liệu đã bị loại bỏ.


    # original_records
    suppression_percent = (
        suppressed_records
        /
        original_records
        *
        100
    )

    # 11.4. TÍNH DATA RETENTION

    # Data Retention cho biết
    # sau ẩn danh hóa còn giữ lại bao nhiêu % dữ liệu.
    #
    # Công thức:
    #
    # released_records
    # ---------------- × 100
    # original_records
    #
    # Data Retention càng cao
    # → càng ít dữ liệu bị mất.
    data_retention_percent = (
        released_records
        /
        original_records
        *
        100
    )


    # 11.5. KIỂM TRA RELEASE DATA VÀ RETAINED INDICES

    # Mỗi dòng còn lại trong release_data
    # phải tương ứng với đúng một index của dữ liệu gốc.
    retained_indices_match = (
        len(
            release_data
        )
        ==
        len(
            retained_indices
        )
    )


    # Nếu số dòng và số index không khớp,
    # dữ liệu Original và Anonymized sẽ bị lệch nhau
    # khi đánh giá Machine Learning.
    #
    # Vì vậy phải dừng pipeline ngay.
    if not retained_indices_match:

        raise ValueError(
            f"{strategy_name}: "
            "release_data và retained_indices không khớp."
        )


    # 11.6. LƯU KẾT QUẢ CỦA STRATEGY
    # Tạo một dictionary con
    strategy_results[
        strategy_name
    ] = {

        # Dataset đã được ẩn danh hóa
        # và sẵn sàng cho các bước đánh giá tiếp theo.
        "release_data": release_data,

        # Index gốc của các bản ghi
        # không bị Suppression.
        "retained_indices": retained_indices,

        # Tổng số bản ghi bị loại bỏ.
        "suppressed_records": suppressed_records,

        # Tỷ lệ % dữ liệu bị loại bỏ.
        "suppression_percent": suppression_percent,

        # Tỷ lệ % dữ liệu còn giữ lại.
        "data_retention_percent": data_retention_percent
    }


    # 11.7. HIỂN THỊ KẾT QUẢ STRATEGY

    # Hiển thị số dòng và số cột
    # của dữ liệu sau ẩn danh hóa.
    print(
        "Kích thước dữ liệu:",
        release_data.shape
    )


    # Hiển thị số index còn được giữ lại.
    print(
        "Số retained indices:",
        len(
            retained_indices
        )
    )


    # True nghĩa là:
    # số bản ghi Anonymized và index Original
    # đang khớp chính xác về số lượng.
    print(
        "Dataset và retained indices khớp?:",
        retained_indices_match
    )


    # Hiển thị số bản ghi đã bị Suppression.
    print(
        "Suppressed records:",
        suppressed_records
    )


    # Hiển thị tỷ lệ Suppression,
    # làm tròn 2 chữ số thập phân.
    print(
        "Suppression (%):",
        round(
            suppression_percent,
            2
        )
    )


    # Hiển thị tỷ lệ dữ liệu còn được giữ lại.
    print(
        "Data Retention (%):",
        round(
            data_retention_percent,
            2
        )
    )


# 12. KIỂM TRA SAU KHI CHẠY TẤT CẢ STRATEGY

# In tiêu đề báo rằng phần Anonymization
# đã chạy xong.
print(
    "\n===== HOÀN THÀNH ANONYMIZATION ====="
)


# Đếm số Strategy đã có kết quả.
#
# Hiện tại kỳ vọng:
# 2
print(
    "Số Strategy đã chạy:",
    len(
        strategy_results
    )
)


# Hiển thị tên tất cả Strategy
# hiện đang được lưu trong strategy_results.
#
# Kỳ vọng hiện tại:
# ['candidate_1', 'candidate_2']
print(
    "Các Strategy đã có kết quả:",
    list(
        strategy_results.keys()
    )
)
# 13. TỰ ĐỘNG XÁC ĐỊNH QI CỦA TỪNG CANDIDATE

# QI = Quasi-Identifier.
# Đây là các thuộc tính không trực tiếp định danh một người
# nhưng khi kết hợp với nhau có thể làm tăng nguy cơ nhận diện.
#
# Trước đây pipeline viết cứng QI cho strategy_1 và strategy_2.
# Bây giờ engine sẽ tự tạo QI dựa trên cấu hình Candidate.
strategy_qi_map = {}


# Duyệt qua từng Candidate đã được sinh tự động.
for strategy_name in strategy_names:

    # Lấy cấu hình Candidate hiện tại.
    strategy_config = (
        strategy_configs[
            strategy_name
        ]
    )


    # Engine tự xác định danh sách QI tương ứng.
    # Ví dụ:
    # age3     → tuoi_nhom_3
    # age_high → tuoi_nhom_high
    qi_columns = (
        anonymization_engine
        .get_candidate_qi_columns(
            strategy_config
        )
    )


    # Lưu QI của Candidate vào dictionary
    # để bước Privacy Evaluation sử dụng.
    strategy_qi_map[
        strategy_name
    ] = qi_columns


# 13.1. KIỂM TRA QI ĐƯỢC TẠO TỰ ĐỘNG

print(
    "\n===== QI CỦA CÁC CANDIDATE ====="
)


for strategy_name in strategy_names:

    print(
        "\nCandidate:",
        strategy_name
    )

    print(
        "QI:",
        strategy_qi_map[
            strategy_name
        ]
    )


# 14. TỰ ĐỘNG ĐÁNH GIÁ PRIVACY CHO TẤT CẢ CANDIDATE

print(
    "\n===== ĐÁNH GIÁ PRIVACY ====="
)


# Duyệt lần lượt từng Strategy
# đã được chạy ở bước Anonymization phía trên
for strategy_name in strategy_names:

    # Hiển thị Strategy đang được đánh giá
    print(
        "\nStrategy:",
        strategy_name
    )


    # 14.1. LẤY DATASET ĐÃ ẨN DANH

    # Lấy release_data của Strategy hiện tại
    # từ dictionary strategy_results.
    #
    # Đây là dữ liệu sau:
    # Generalization + Suppression.
    release_data = (
        strategy_results[
            strategy_name
        ][
            "release_data"
        ]
    )


    # 14.2. LẤY DANH SÁCH QI

    # Mỗi Strategy có danh sách QI tương ứng.
    #
    # Ví dụ:
    # candidate_1 (age3)
    # → tuoi_nhom_3
    #
    # candidate_2 (age_high)
    # → tuoi_nhom_high
    qi_columns = (
        strategy_qi_map[
            strategy_name
        ]
    )


    # 14.3. KIỂM TRA CÁC CỘT QI CÓ TỒN TẠI KHÔNG

    # Tìm những cột QI được khai báo
    # nhưng không xuất hiện trong release_data.
    missing_qi_columns = [
        column
        for column in qi_columns
        if column not in release_data.columns
    ]


    # Nếu có cột QI bị thiếu,
    # dừng pipeline để tránh đánh giá Privacy sai.
    if missing_qi_columns:

        raise ValueError(
            f"{strategy_name}: "
            f"Thiếu các cột QI {missing_qi_columns}"
        )


    # 14.4. ĐÁNH GIÁ k-ANONYMITY VÀ l-DIVERSITY

    # Gọi hàm evaluate_privacy_full()
    privacy_result = (
        privacy_analyzer.evaluate_privacy_full(

            # Dataset đã ẩn danh
            dataframe=release_data,

            # Danh sách Quasi-Identifier
            qi_columns=qi_columns,

            # Thuộc tính nhạy cảm cần bảo vệ
            sensitive_column="thu_nhap",

            # Ngưỡng k thực nghiệm của đồ án
            k_required=5,

            # Ngưỡng l thực nghiệm của đồ án
            l_required=2
        )
    )


    # 14.5. LƯU KẾT QUẢ PRIVACY
    # Bổ sung kết quả Privacy vào đúng Strategy.
    #
    # Sau bước này sẽ có:
    #
    # strategy_results["candidate_1"]["privacy"]
    #
    # và:
    #
    # strategy_results["candidate_2"]["privacy"]
    strategy_results[
        strategy_name
    ][
        "privacy"
    ] = privacy_result


    # 14.6. HIỂN THỊ KẾT QUẢ PRIVACY

    # Hiển thị giá trị k nhỏ nhất
    # trong toàn bộ equivalence class.
    print(
        "k_min:",
        privacy_result[
            "k_min"
        ]
    )


    # True nghĩa là đạt yêu cầu k >= 5.
    print(
        "k_valid:",
        privacy_result[
            "k_valid"
        ]
    )


    # Hiển thị số bản ghi còn vi phạm k.
    #
    # Sau khi Suppression đúng,
    # kỳ vọng bằng 0.
    print(
        "Số bản ghi vi phạm k:",
        privacy_result[
            "so_ban_ghi_vi_pham_k"
        ]
    )


    # Hiển thị l nhỏ nhất
    # của các equivalence class.
    print(
        "l_min:",
        privacy_result[
            "l_min"
        ]
    )


    # True nghĩa là đạt yêu cầu l >= 2.
    print(
        "l_valid:",
        privacy_result[
            "l_valid"
        ]
    )


    # Hiển thị số nhóm còn vi phạm l-diversity.
    #
    # Sau khi Suppression đúng,
    # kỳ vọng bằng 0.
    print(
        "Số nhóm vi phạm l:",
        privacy_result[
            "so_nhom_vi_pham_l"
        ]
    )


    # Hiển thị số bản ghi còn nằm
    # trong các nhóm vi phạm l-diversity.
    print(
        "Số bản ghi vi phạm l:",
        privacy_result[
            "so_ban_ghi_vi_pham_l"
        ]
    )


    # Kết luận cuối cùng về Privacy
    # theo tiêu chí đang sử dụng trong đồ án.
    #
    # True chỉ khi:
    # k_valid == True
    # và
    # l_valid == True
    print(
        "Privacy valid:",
        privacy_result[
            "privacy_valid"
        ]
    )


# 15. KIỂM TRA ĐÃ LƯU PRIVACY CHƯA

print(
    "\n===== HOÀN THÀNH PRIVACY EVALUATION ====="
)


# Kiểm tra mỗi Strategy đã có key "privacy" hay chưa.
for strategy_name in strategy_names:

    print(
        strategy_name,
        "- đã có Privacy?:",
        "privacy"
        in strategy_results[
            strategy_name
        ]
    )
# 16. MACHINE LEARNING VALIDATION CHO TẤT CẢ CANDIDATE



print(
    "\n===== MACHINE LEARNING VALIDATION ====="
)


# Duyệt lần lượt tất cả Strategy
# đã được ẩn danh và đánh giá Privacy.
for strategy_name in strategy_names:

    # Hiển thị Strategy đang được đánh giá ML.
    print(
        "\nStrategy:",
        strategy_name
    )


    # 16.1. LẤY DỮ LIỆU CỦA STRATEGY

    # Lấy dataset đã được ẩn danh hóa.
    release_data = (
        strategy_results[
            strategy_name
        ][
            "release_data"
        ]
    )


    # Lấy index gốc của những bản ghi
    # còn được giữ lại sau Suppression.
    #
    # Các index này giúp đảm bảo:
    # Original và Anonymized được đánh giá
    # trên đúng cùng một nhóm bản ghi.
    retained_indices = (
        strategy_results[
            strategy_name
        ][
            "retained_indices"
        ]
    )


    # 16.2. CHẠY MACHINE LEARNING VALIDATION
    # Hàm evaluate_strategy_validation()
    # đã được xây dựng trong ml_evaluator.py.

    ml_validation_result = (
        ml_evaluator.evaluate_strategy_validation(

            # Dataset gốc đầy đủ
            original_dataframe=data,

            # Dataset đã ẩn danh của Strategy hiện tại
            anonymized_dataframe=release_data,

            # Index của các bản ghi còn được giữ lại
            retained_indices=retained_indices,

            # Cột mục tiêu của bài toán phân loại
            target_column="thu_nhap",

            # Cố định random_state
            # để kết quả có thể tái lập
            random_state=42
        )
    )


    # 16.3. LƯU KẾT QUẢ ML VALIDATION

    strategy_results[
        strategy_name
    ][
        "ml_validation"
    ] = ml_validation_result


    # Lưu riêng Utility Score
    # để bước Strategy Selection phía sau
    # có thể lấy trực tiếp mà không cần đào sâu dictionary.
    strategy_results[
        strategy_name
    ][
        "utility_score_percent"
    ] = (
        ml_validation_result[
            "utility_score_percent"
        ]
    )


    # 16.4. LẤY METRIC ORIGINAL VÀ ANONYMIZED

    # Metric của mô hình sử dụng dữ liệu gốc.
    original_metrics = (
        ml_validation_result[
            "original_metrics"
        ]
    )


    # Metric của mô hình sử dụng dữ liệu đã ẩn danh.
    anonymized_metrics = (
        ml_validation_result[
            "anonymized_metrics"
        ]
    )

    # 16.5. HIỂN THỊ KẾT QUẢ

    # Accuracy của dữ liệu Original.
    print(
        "Original Accuracy (%):",
        round(
            original_metrics[
                "accuracy"
            ]
            *
            100,
            2
        )
    )


    # Accuracy của dữ liệu Anonymized.
    print(
        "Anonymized Accuracy (%):",
        round(
            anonymized_metrics[
                "accuracy"
            ]
            *
            100,
            2
        )
    )


    # Utility Score tổng hợp.
    #
    # Utility càng gần 100%
    # nghĩa là dữ liệu sau ẩn danh
    # vẫn giữ được khả năng phục vụ Machine Learning tốt.
    print(
        "Validation Utility Score (%):",
        round(
            ml_validation_result[
                "utility_score_percent"
            ],
            2
        )
    )


    # Hiển thị số bản ghi Validation.
    print(
        "Validation size:",
        len(
            ml_validation_result[
                "validation_indices"
            ]
        )
    )


    # Hiển thị số bản ghi Test đã được dành riêng.
    #
    # Lưu ý:
    # các bản ghi Test này CHƯA được dùng
    # để lựa chọn Strategy.
    print(
        "Reserved Test size:",
        len(
            ml_validation_result[
                "test_indices"
            ]
        )
    )


# 17. KIỂM TRA ML VALIDATION ĐÃ ĐƯỢC LƯU
print(
    "\n===== HOÀN THÀNH ML VALIDATION ====="
)


# Kiểm tra từng Strategy
# đã có kết quả ML Validation hay chưa.
for strategy_name in strategy_names:

    print(
        strategy_name,
        "- đã có ML Validation?:",
        "ml_validation"
        in strategy_results[
            strategy_name
        ]
    )
# 18. CHUẨN BỊ DỮ LIỆU ĐỂ XẾP HẠNG CANDIDATE



strategies_for_selection = []


# Duyệt qua từng Strategy đang có trong hệ thống.
for strategy_name in strategy_names:

    # 18.1. LẤY KẾT QUẢ CỦA STRATEGY HIỆN TẠI

    # current_result là dictionary chứa toàn bộ kết quả
    # đã tích lũy của Strategy hiện tại.
    current_result = (
        strategy_results[
            strategy_name
        ]
    )


    # 18.2. TẠO DỮ LIỆU ĐẦU VÀO CHO STRATEGY SELECTOR


    strategy_summary = {

        # Tên Strategy
        "strategy":
            strategy_name,

        # Tỷ lệ bản ghi bị loại bỏ
        # trong quá trình Suppression.
        #
        # Ví dụ:
        # Strategy 1 ≈ 6.01%
        # Strategy 2 ≈ 12.98%
        "suppression_percent":
            current_result[
                "suppression_percent"
            ],

        # Utility Score lấy từ
        # Machine Learning Validation.
        #
        # Giá trị càng gần 100%
        # nghĩa là dữ liệu sau ẩn danh
        # càng giữ được khả năng sử dụng cho ML.
        "utility_score_percent":
            current_result[
                "utility_score_percent"
            ],

        # Kết quả kiểm tra Privacy.
        #
        # True nghĩa là Strategy đạt
        # k=5 và l=2 theo tiêu chí thực nghiệm của đồ án.
        "privacy_valid":
            current_result[
                "privacy"
            ][
                "privacy_valid"
            ]
    }


    # 18.3. THÊM STRATEGY VÀO DANH SÁCH XẾP HẠNG

    strategies_for_selection.append(
        strategy_summary
    )


# 19. XẾP HẠNG TẤT CẢ CANDIDATE

ranked_strategies = (
    strategy_selector.rank_strategies(

        # Danh sách các Strategy cần đánh giá
        strategies_for_selection,

        # Trọng số cho khả năng giữ lại dữ liệu
        weight_data_retention=0.5,

        # Trọng số cho khả năng giữ Utility
        weight_utility=0.5
    )
)


# 20. HIỂN THỊ BẢNG XẾP HẠNG CANDIDATE

print(
    "\n===== XẾP HẠNG CANDIDATE ====="
)


# rank_strategies() trả về một danh sách
# đã được sắp xếp theo thứ hạng.
#
# Ta duyệt từng kết quả để hiển thị.
for result in ranked_strategies:

    # 20.1. THỨ HẠNG

    print(
        "\nRank:",
        result[
            "rank"
        ]
    )


    # 20.2. TÊN STRATEGY

    print(
        "Strategy:",
        result[
            "strategy"
        ]
    )

    # 20.3. PRIVACY

    # True nghĩa là Strategy đủ điều kiện Privacy
    # theo k=5 và l=2 của thực nghiệm.
    print(
        "Privacy valid:",
        result[
            "privacy_valid"
        ]
    )


    # 20.4. SUPPRESSION

    # Đây là tỷ lệ dữ liệu bị loại bỏ.
    print(
        "Suppression (%):",
        round(
            result[
                "suppression_%"
            ],
            2
        )
    )


    # 20.5. DATA RETENTION

    # Đây là tỷ lệ dữ liệu còn được giữ lại.
    #
    # Công thức về bản chất là:
    #
    # Data Retention = 100 - Suppression
    print(
        "Data Retention (%):",
        round(
            result[
                "data_retention_%"
            ],
            2
        )
    )


    # 20.6. UTILITY

    # Utility Score được lấy từ
    # kết quả Machine Learning Validation.
    print(
        "Utility Score (%):",
        round(
            result[
                "utility_score_%"
            ],
            2
        )
    )


    # 20.7. SELECTION SCORE

    # Selection Score hiện được tính từ:
    #
    # 50% Data Retention
    # +
    # 50% Utility
    #
    # Strategy có Selection Score cao hơn
    # sẽ được ưu tiên hơn,
    # với điều kiện Strategy đạt Privacy.
    print(
        "Selection Score:",
        round(
            result[
                "selection_score"
            ],
            2
        )
    )


    # 20.8. ELIGIBLE

    # eligible=True:
    # Strategy đủ điều kiện tham gia lựa chọn.
    #
    # Với logic hiện tại,
    # Strategy không đạt Privacy
    # sẽ không được xem là phương án hợp lệ.
    print(
        "Eligible:",
        result[
            "eligible"
        ]
    )
# 20.9. SENSITIVITY ANALYSIS CHO TRỌNG SỐ SELECTION SCORE

print(
    "\n===== SENSITIVITY ANALYSIS CHO TRỌNG SỐ =====\n"
)


sensitivity_results = (
    strategy_selector.run_weight_sensitivity_analysis(
        strategies=strategies_for_selection
    )
)


# Chuyển sang DataFrame để dễ xem và xuất file.
sensitivity_dataframe = pd.DataFrame(
    sensitivity_results
)


print(
    sensitivity_dataframe.to_string(
        index=False
    )
)


# Kiểm tra Candidate đứng hạng 1 có ổn định
# xuyên suốt mọi bộ trọng số hay không.
stability_result = (
    strategy_selector.is_best_strategy_stable(
        sensitivity_results
    )
)


print(
    "\nCandidate hạng 1 có ổn định qua mọi bộ trọng số?:",
    stability_result["is_stable"]
)


print(
    "Các Candidate từng đứng hạng 1 ở ít nhất 1 bộ trọng số:",
    stability_result["strategies_that_won"]
)



sensitivity_output_dir = (
    PROJECT_ROOT
    / "outputs_bieu_do_ket_qua"
)


sensitivity_output_dir.mkdir(
    parents=True,
    exist_ok=True
)


SENSITIVITY_FILE = (
    sensitivity_output_dir
    / "sensitivity_analysis_trong_so.csv"
)


sensitivity_dataframe.to_csv(
    SENSITIVITY_FILE,
    index=False
)


print(
    "\nĐã lưu Sensitivity Analysis tại:",
    SENSITIVITY_FILE
)


# 21. TỰ ĐỘNG CHỌN CANDIDATE TỐT NHẤT

best_strategy = (
    strategy_selector.select_best_strategy(

        # Danh sách Strategy đã chuẩn bị
        # ở bước 18
        strategies_for_selection,

        # Trọng số cho khả năng giữ lại dữ liệu
        weight_data_retention=0.5,

        # Trọng số cho Utility
        weight_utility=0.5
    )
)


# 22. LẤY TÊN STRATEGY ĐƯỢC CHỌN

# best_strategy là dictionary chứa
# thông tin của Strategy tốt nhất.
#
# Ta lấy riêng tên Strategy
# để sử dụng cho các bước tiếp theo.
selected_strategy_name = (
    best_strategy[
        "strategy"
    ]
)


# 23. LẤY DỮ LIỆU CỦA STRATEGY ĐƯỢC CHỌN

# Lấy dataset đã ẩn danh
# của Strategy được hệ thống lựa chọn.
selected_release_data = (
    strategy_results[
        selected_strategy_name
    ][
        "release_data"
    ]
)


# Lấy các index gốc còn được giữ lại
# của Strategy được chọn.
selected_retained_indices = (
    strategy_results[
        selected_strategy_name
    ][
        "retained_indices"
    ]
)


# Lấy kết quả ML Validation
# đã được tính trước đó cho Strategy được chọn.

selected_ml_result = (
    strategy_results[
        selected_strategy_name
    ][
        "ml_validation"
    ]
)


# 24. HIỂN THỊ STRATEGY ĐƯỢC HỆ THỐNG CHỌN

print(
    "\n===== CANDIDATE ĐƯỢC LỰA CHỌN ====="
)


print(
    "Selected Strategy:",
    selected_strategy_name
)


print(
    "Selection Score:",
    round(
        best_strategy[
            "selection_score"
        ],
        2
    )
)


print(
    "Privacy valid:",
    best_strategy[
        "privacy_valid"
    ]
)


print(
    "Data Retention (%):",
    round(
        best_strategy[
            "data_retention_%"
        ],
        2
    )
)


print(
    "Utility Score (%):",
    round(
        best_strategy[
            "utility_score_%"
        ],
        2
    )
)


print(
    "Kích thước dữ liệu được chọn:",
    selected_release_data.shape
)


print(
    "Số retained indices:",
    len(
        selected_retained_indices
    )
)


print(
    "Reserved Test size:",
    len(
        selected_ml_result[
            "test_indices"
        ]
    )
)


# 25. FINAL TEST CHO STRATEGY ĐƯỢC HỆ THỐNG CHỌN


# Sau khi Strategy tốt nhất đã được lựa chọn
# bằng tập Validation,
# bây giờ ta mới sử dụng tập Test cuối cùng.


print(
    "\n===== FINAL TEST ====="
)


# Gọi hàm evaluate_selected_strategy_test()
# đã xây dựng trong ml_evaluator.py.

final_test_result = (
    ml_evaluator.evaluate_selected_strategy_test(

        # Dataset gốc đầy đủ
        original_dataframe=data,

        # Dataset đã ẩn danh của Strategy được chọn
        anonymized_dataframe=selected_release_data,

        # Index các bản ghi còn lại
        # sau quá trình Suppression
        retained_indices=selected_retained_indices,

        # Kết quả Validation của Strategy được chọn.
        #
        # Trong đó đã chứa:
        # - test_indices
        # - original_model_pipeline
        # - anonymized_model_pipeline
        validation_result=selected_ml_result,

        # Cột mục tiêu cần dự đoán
        target_column="thu_nhap"
    )
)



# 26. LƯU KẾT QUẢ FINAL TEST
strategy_results[
    selected_strategy_name
][
    "final_test"
] = final_test_result


# 27. LẤY CÁC METRIC FINAL TEST

# Metric của mô hình sử dụng dữ liệu Original
original_test_metrics = (
    final_test_result[
        "original_metrics"
    ]
)


# Metric của mô hình sử dụng dữ liệu Anonymized
anonymized_test_metrics = (
    final_test_result[
        "anonymized_metrics"
    ]
)


# 28. HIỂN THỊ KẾT QUẢ FINAL TEST

# Hiển thị Strategy đang được Test
print(
    "Strategy:",
    selected_strategy_name
)


# Số lượng bản ghi trong tập Test
print(
    "Test size:",
    final_test_result[
        "test_size"
    ]
)


# Kiểm tra Original và Anonymized
# có sử dụng đúng cùng một tập index hay không.
print(
    "Cùng Test indices?:",
    final_test_result[
        "same_test_indices"
    ]
)


# Kiểm tra nhãn thu_nhap của hai dataset
# có khớp hoàn toàn hay không.

print(
    "Cùng Test target?:",
    final_test_result[
        "same_test_target"
    ]
)


# ACCURACY

print(
    "Original Accuracy (%):",
    round(
        original_test_metrics[
            "accuracy"
        ]
        *
        100,
        2
    )
)


print(
    "Anonymized Accuracy (%):",
    round(
        anonymized_test_metrics[
            "accuracy"
        ]
        *
        100,
        2
    )
)


# F1-SCORE

print(
    "Original F1 Score (%):",
    round(
        original_test_metrics[
            "f1_score"
        ]
        *
        100,
        2
    )
)


print(
    "Anonymized F1 Score (%):",
    round(
        anonymized_test_metrics[
            "f1_score"
        ]
        *
        100,
        2
    )
)


# FINAL UTILITY SCORE

print(
    "Final Test Utility Score (%):",
    round(
        final_test_result[
            "utility_score_percent"
        ],
        2
    )
)


# KIỂM TRA ĐÃ LƯU KẾT QUẢ FINAL TEST

print(
    "Đã lưu final_test?:",
    "final_test"
    in strategy_results[
        selected_strategy_name
    ]
)
# 29. XÁC ĐỊNH THƯ MỤC LƯU DỮ LIỆU ẨN DANH CUỐI CÙNG

PROCESSED_DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed_da_xu_li"
)


# 30. TẠO THƯ MỤC NẾU CHƯA TỒN TẠI

#
PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)



# 31. XÁC ĐỊNH TÊN FILE DỮ LIỆU CUỐI CÙNG

# File dữ liệu ẩn danh cuối cùng
# sẽ được lưu với tên cố định này.
FINAL_ANONYMIZED_FILE = (
    PROCESSED_DATA_DIR
    / "du_lieu_an_danh_cuoi_cung.csv"
)



# 32. LƯU DATASET ẨN DANH CUỐI CÙNG

#
selected_release_data.to_csv(
    FINAL_ANONYMIZED_FILE,
    index=False
)



# 33. ĐỌC LẠI FILE ĐỂ KIỂM TRA


#
saved_anonymized_data = pd.read_csv(
    FINAL_ANONYMIZED_FILE
)



# 34. KIỂM TRA KẾT QUẢ XUẤT FILE


print(
    "\n===== XUẤT DATASET ẨN DANH CUỐI CÙNG ====="
)


# Hiển thị Strategy tạo ra dataset cuối.
print(
    "Strategy được sử dụng:",
    selected_strategy_name
)


# Hiển thị đường dẫn file đã lưu.
print(
    "Đường dẫn file:",
    FINAL_ANONYMIZED_FILE
)


# Kiểm tra file có thực sự tồn tại không.
print(
    "File tồn tại?:",
    FINAL_ANONYMIZED_FILE.exists()
)


# Hiển thị kích thước dataset
# sau khi đọc lại từ file CSV.
print(
    "Kích thước file đã lưu:",
    saved_anonymized_data.shape
)


# Kiểm tra kích thước dữ liệu lưu ra
# có giống dữ liệu trước khi lưu không.
same_shape = (
    saved_anonymized_data.shape
    ==
    selected_release_data.shape
)


print(
    "Kích thước dữ liệu khớp?:",
    same_shape
)


# Nếu kích thước không khớp,
# dừng pipeline để tránh sử dụng file sai.
if not same_shape:

    raise ValueError(
        "Dataset sau khi lưu có kích thước không khớp "
        "với dataset ẩn danh được lựa chọn."
    )


# Hiển thị danh sách các cột
# để kiểm tra không xuất hiện cột index thừa.
print(
    "Các cột trong file cuối:"
)

print(
    saved_anonymized_data.columns.tolist()
)


print(
    "Xuất dataset cuối cùng: THÀNH CÔNG"
)
# 35. TẠO THƯ MỤC LƯU KẾT QUẢ TỔNG HỢP
# - kết quả tổng hợp hệ thống
# - biểu đồ
# - các bảng số liệu phục vụ báo cáo đồ án
OUTPUT_DIR = (
    PROJECT_ROOT
    / "outputs_bieu_do_ket_qua"
)


# Nếu thư mục chưa tồn tại
# thì tự động tạo.
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# 36. LẤY CÁC KẾT QUẢ CỦA STRATEGY CUỐI CÙNG
# Lấy toàn bộ kết quả của Strategy
# đã được hệ thống tự động lựa chọn.
selected_strategy_result = (
    strategy_results[
        selected_strategy_name
    ]
)


# Lấy kết quả Privacy.
selected_privacy = (
    selected_strategy_result[
        "privacy"
    ]
)


# Lấy kết quả Final Test.
selected_final_test = (
    selected_strategy_result[
        "final_test"
    ]
)


# Lấy metric Original trên tập Test.
final_original_metrics = (
    selected_final_test[
        "original_metrics"
    ]
)


# Lấy metric Anonymized trên tập Test.
final_anonymized_metrics = (
    selected_final_test[
        "anonymized_metrics"
    ]
)


# Lấy các tỷ lệ Utility Retention.
final_utility_result = (
    selected_final_test[
        "utility_result"
    ]
)


# 37. TẠO BẢNG TỔNG HỢP KẾT QUẢ HỆ THỐNG

final_system_summary = {

    # THÔNG TIN STRATEGY

    "selected_strategy":
        selected_strategy_name,

    "original_records":
        len(data),

    "released_records":
        len(selected_release_data),

    "suppressed_records":
        selected_strategy_result[
            "suppressed_records"
        ],

    "suppression_percent":
        round(
            selected_strategy_result[
                "suppression_percent"
            ],
            2
        ),

    "data_retention_percent":
        round(
            selected_strategy_result[
                "data_retention_percent"
            ],
            2
        ),


    # PRIVACY

    "privacy_valid":
        selected_privacy[
            "privacy_valid"
        ],

    "k_min":
        selected_privacy[
            "k_min"
        ],

    "k_required":
        selected_privacy[
            "k_required"
        ],

    "k_valid":
        selected_privacy[
            "k_valid"
        ],

    "records_violating_k":
        selected_privacy[
            "so_ban_ghi_vi_pham_k"
        ],

    "l_min":
        selected_privacy[
            "l_min"
        ],

    "l_required":
        selected_privacy[
            "l_required"
        ],

    "l_valid":
        selected_privacy[
            "l_valid"
        ],

    "groups_violating_l":
        selected_privacy[
            "so_nhom_vi_pham_l"
        ],

    "records_violating_l":
        selected_privacy[
            "so_ban_ghi_vi_pham_l"
        ],


    # STRATEGY SELECTION

    "validation_utility_score_percent":
        round(
            selected_strategy_result[
                "utility_score_percent"
            ],
            2
        ),

    "selection_score":
        round(
            best_strategy[
                "selection_score"
            ],
            2
        ),


    # FINAL TEST

    "test_size":
        selected_final_test[
            "test_size"
        ],

    "final_test_utility_score_percent":
        round(
            selected_final_test[
                "utility_score_percent"
            ],
            2
        ),


    # ORIGINAL TEST METRICS

    "original_test_accuracy_percent":
        round(
            final_original_metrics["accuracy"] * 100,
            2
        ),

    "original_test_precision_percent":
        round(
            final_original_metrics["precision"] * 100,
            2
        ),

    "original_test_recall_percent":
        round(
            final_original_metrics["recall"] * 100,
            2
        ),

    "original_test_f1_percent":
        round(
            final_original_metrics["f1_score"] * 100,
            2
        ),

    "original_test_balanced_accuracy_percent":
        round(
            final_original_metrics[
                "balanced_accuracy"
            ] * 100,
            2
        ),

    "original_test_roc_auc_percent":
        round(
            final_original_metrics["roc_auc"] * 100,
            2
        ),


    # ANONYMIZED TEST METRICS

    "anonymized_test_accuracy_percent":
        round(
            final_anonymized_metrics["accuracy"] * 100,
            2
        ),

    "anonymized_test_precision_percent":
        round(
            final_anonymized_metrics["precision"] * 100,
            2
        ),

    "anonymized_test_recall_percent":
        round(
            final_anonymized_metrics["recall"] * 100,
            2
        ),

    "anonymized_test_f1_percent":
        round(
            final_anonymized_metrics["f1_score"] * 100,
            2
        ),

    "anonymized_test_balanced_accuracy_percent":
        round(
            final_anonymized_metrics[
                "balanced_accuracy"
            ] * 100,
            2
        ),

    "anonymized_test_roc_auc_percent":
        round(
            final_anonymized_metrics["roc_auc"] * 100,
            2
        ),


    # UTILITY RETENTION

    "accuracy_retention_percent":
        round(
            final_utility_result[
                "accuracy_retention_%"
            ],
            2
        ),

    "f1_retention_percent":
        round(
            final_utility_result[
                "f1_retention_%"
            ],
            2
        ),

    "balanced_accuracy_retention_percent":
        round(
            final_utility_result[
                "balanced_accuracy_retention_%"
            ],
            2
        ),

    "roc_auc_retention_percent":
        round(
            final_utility_result[
                "roc_auc_retention_%"
            ],
            2
        )
}


# 38. LƯU KẾT QUẢ TỔNG HỢP RA FILE CSV

# Chuyển dictionary thành DataFrame 1 dòng.
summary_dataframe = pd.DataFrame(
    [
        final_system_summary
    ]
)


# Đường dẫn file kết quả tổng hợp.
FINAL_SUMMARY_FILE = (
    OUTPUT_DIR
    / "ket_qua_tong_hop_he_thong.csv"
)


# Lưu ra CSV.
summary_dataframe.to_csv(
    FINAL_SUMMARY_FILE,
    index=False
)


# 39. KIỂM TRA FILE KẾT QUẢ

print(
    "\n===== XUẤT KẾT QUẢ TỔNG HỢP ====="
)


print(
    "Đường dẫn:",
    FINAL_SUMMARY_FILE
)


print(
    "File tồn tại?:",
    FINAL_SUMMARY_FILE.exists()
)


print(
    "Kích thước bảng tổng hợp:",
    summary_dataframe.shape
)


print(
    "Selected Strategy:",
    final_system_summary[
        "selected_strategy"
    ]
)


print(
    "Privacy valid:",
    final_system_summary[
        "privacy_valid"
    ]
)


print(
    "Final Test Utility (%):",
    final_system_summary[
        "final_test_utility_score_percent"
    ]
)


print(
    "Xuất kết quả tổng hợp: THÀNH CÔNG"
)

candidate_ranking_rows = []


# 40.1. DUYỆT KẾT QUẢ ĐÃ ĐƯỢC XẾP HẠNG

for ranked_result in ranked_strategies:

    # LẤY TÊN CANDIDATE

    candidate_name = (
        ranked_result[
            "strategy"
        ]
    )


    # LẤY CẤU HÌNH GENERALIZATION

    candidate_config = (
        strategy_configs[
            candidate_name
        ]
    )


    # TẠO MỘT DÒNG KẾT QUẢ

    candidate_row = {

        # Thứ hạng Candidate.
        "rank":
            ranked_result[
                "rank"
            ],

        # Tên Candidate.
        "strategy":
            candidate_name,

        # Mức Generalization tuổi.
        "age_level":
            candidate_config[
                "age_level"
            ],

        # Mức Generalization giờ làm việc.
        "hours_level":
            candidate_config[
                "hours_level"
            ],

        # Candidate có đạt Privacy
        # theo tiêu chí k=5 và l=2 hay không.
        "privacy_valid":
            ranked_result[
                "privacy_valid"
            ],

        # Tỷ lệ dữ liệu bị loại bỏ.
        "suppression_percent":
            round(
                ranked_result[
                    "suppression_%"
                ],
                2
            ),

        # Tỷ lệ dữ liệu còn được giữ lại.
        "data_retention_percent":
            round(
                ranked_result[
                    "data_retention_%"
                ],
                2
            ),

        # Utility Score trên tập Validation.
        "utility_score_percent":
            round(
                ranked_result[
                    "utility_score_%"
                ],
                2
            ),

        # Selection Score dùng để xếp hạng.
        "selection_score":
            round(
                ranked_result[
                    "selection_score"
                ],
                2
            ),

        # Candidate có đủ điều kiện
        # tham gia lựa chọn cuối cùng hay không.
        "eligible":
            ranked_result[
                "eligible"
            ]
    }


    # Thêm dòng vừa tạo
    # vào danh sách chung.
    candidate_ranking_rows.append(
        candidate_row
    )

# 41. CHUYỂN THÀNH DATAFRAME

candidate_ranking_dataframe = (
    pd.DataFrame(
        candidate_ranking_rows
    )
)


# 42. XÁC ĐỊNH ĐƯỜNG DẪN FILE

CANDIDATE_RANKING_FILE = (
    OUTPUT_DIR
    / "bang_xep_hang_candidate.csv"
)


# 43. LƯU BẢNG XẾP HẠNG RA CSV

candidate_ranking_dataframe.to_csv(
    CANDIDATE_RANKING_FILE,
    index=False
)


# 44. KIỂM TRA KẾT QUẢ


print(
    "\n===== XUẤT BẢNG XẾP HẠNG CANDIDATE ====="
)


print(
    "Đường dẫn:",
    CANDIDATE_RANKING_FILE
)


print(
    "File tồn tại?:",
    CANDIDATE_RANKING_FILE.exists()
)


print(
    "Kích thước bảng:",
    candidate_ranking_dataframe.shape
)


print(
    "\nBảng xếp hạng:"
)


# In toàn bộ DataFrame
# để kiểm tra trực tiếp trên Console.
print(
    candidate_ranking_dataframe.to_string(
        index=False
    )
)


print(
    "\nXuất bảng xếp hạng Candidate: Chúc mừng bạn đã chạy thành công"
)
