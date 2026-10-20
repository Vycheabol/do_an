# Mục đích:
# Chứa các hàm phục vụ đánh giá ảnh hưởng của quá trình
# ẩn danh hóa lên hiệu quả của mô hình Machine Learning.
#
# Module này sẽ giúp hệ thống:
# - lấy đúng các bản ghi gốc tương ứng với dữ liệu ẩn danh
# - chia Train / Validation / Test
# - lấy các tập dữ liệu theo cùng index
# - chuẩn bị feature và target của dữ liệu gốc
#
# Các bước tiền xử lý, huấn luyện Logistic Regression
# và tính Utility Score sẽ được bổ sung ở các bước tiếp theo.


# Import pandas để xử lý dữ liệu dạng DataFrame
import pandas as pd


import numpy as np



from sklearn.model_selection import train_test_split



from sklearn.compose import ColumnTransformer



from sklearn.pipeline import Pipeline


# Import SimpleImputer để xử lý các giá trị bị thiếu
from sklearn.impute import SimpleImputer


# Import OneHotEncoder để chuyển dữ liệu phân loại
# thành dạng số mà mô hình Machine Learning có thể sử dụng
from sklearn.preprocessing import OneHotEncoder


# Import StandardScaler để chuẩn hóa các cột dạng số
from sklearn.preprocessing import StandardScaler


# Import LogisticRegression
# Đây là mô hình đã được chọn từ quá trình thử nghiệm trước
# dựa trên kết quả ở tập Validation
from sklearn.linear_model import LogisticRegression


# Import module utility_evaluator của dự án
# Module này chứa các hàm tính metric và Utility Score
import utility_evaluator



# LẤY DỮ LIỆU GỐC TƯƠNG ỨNG VỚI DỮ LIỆU ẨN DANH

# Tạo hàm get_aligned_original_data()
# để lấy đúng những bản ghi trong dữ liệu gốc
# vẫn còn tồn tại sau quá trình suppression
def get_aligned_original_data(
    original_dataframe,
    retained_indices
):

    # Dùng .loc[] để lấy đúng các dòng dữ liệu gốc
    # dựa trên index mà anonymization_engine trả về
    aligned_original_data = (
        original_dataframe
        .loc[
            retained_indices
        ]
        .copy()
    )


    # Trả về dữ liệu gốc đã được căn chỉnh
    # với dữ liệu ẩn danh của strategy đang xét
    return aligned_original_data



# CHIA INDEX THÀNH TRAIN / VALIDATION / TEST


# Tạo hàm split_train_validation_test_indices()
# để chia dữ liệu theo đúng quy trình đã dùng trước đây:
#
# Train      = 60%
# Validation = 20%
# Test       = 20%
#
# Chúng ta chia INDEX để Original và Anonymized
# luôn dùng đúng cùng các bản ghi
def split_train_validation_test_indices(
    dataframe,
    target_column="thu_nhap",
    random_state=42
):

    # Lấy toàn bộ index của DataFrame
    # Đây là index gốc của các bản ghi còn được giữ lại
    all_indices = dataframe.index


    # Lấy cột target để dùng stratify
    # Stratify giúp giữ tỷ lệ <=50K và >50K
    # tương đối ổn định giữa các tập dữ liệu
    target = dataframe[
        target_column
    ]


    # BƯỚC 1:
    # CHIA 60% TRAIN VÀ 40% TEMP


    # Chia lần thứ nhất thành:
    # - 60% Train
    # - 40% Temp
    train_indices, temp_indices = train_test_split(

        # Chia dựa trên index của dữ liệu
        all_indices,

        # 40% dữ liệu được dành cho Temp
        test_size=0.40,

        # Giữ tỷ lệ hai lớp thu_nhap ổn định
        stratify=target,

        # Cố định kết quả để có thể tái lập thí nghiệm
        random_state=random_state
    )


    # Lấy target tương ứng với tập Temp
    # để tiếp tục stratify ở lần chia thứ hai
    temp_target = dataframe.loc[
        temp_indices,
        target_column
    ]


    # BƯỚC 2:
    # CHIA TEMP THÀNH VALIDATION VÀ TEST


    # Chia 40% Temp thành hai phần bằng nhau:
    # - 20% Validation
    # - 20% Test
    validation_indices, test_indices = train_test_split(

        # Chia trên index của tập Temp
        temp_indices,

        # Lấy 50% của Temp làm Test
        # 50% của 40% = 20% toàn bộ dữ liệu
        test_size=0.50,

        # Giữ tỷ lệ hai lớp thu_nhap ổn định
        stratify=temp_target,

        # Dùng cùng random_state như lần chia thứ nhất
        random_state=random_state
    )


    # Trả về đúng thứ tự:
    # Train -> Validation -> Test
    return (
        train_indices,
        validation_indices,
        test_indices
    )


# HÀM 3:
# LẤY TRAIN / VALIDATION / TEST THEO INDEX ĐÃ CHIA



# Tạo hàm get_data_splits_by_indices()
# để lấy dữ liệu Train, Validation và Test
# dựa trên các bộ index đã được chia ở hàm phía trên
def get_data_splits_by_indices(
    dataframe,
    train_indices,
    validation_indices,
    test_indices
):

    # Lấy các dòng thuộc tập Train
    # .copy() tạo một DataFrame độc lập để xử lý sau này
    train_data = (
        dataframe
        .loc[
            train_indices
        ]
        .copy()
    )


    # Lấy các dòng thuộc tập Validation
    validation_data = (
        dataframe
        .loc[
            validation_indices
        ]
        .copy()
    )


    # Lấy các dòng thuộc tập Test
    test_data = (
        dataframe
        .loc[
            test_indices
        ]
        .copy()
    )


    # Trả về lần lượt:
    # Train -> Validation -> Test
    return (
        train_data,
        validation_data,
        test_data
    )


# HÀM 4:
# CHUẨN BỊ FEATURE VÀ TARGET CỦA DỮ LIỆU GỐC


# Tạo hàm prepare_original_features_target()
# để:
# - lấy đúng 7 feature gốc sử dụng cho Machine Learning
# - tách riêng cột target thu_nhap
# - chuyển dấu ? thành missing value
def prepare_original_features_target(
    dataframe,
    target_column="thu_nhap"
):

    # Khai báo đúng 7 feature của dữ liệu gốc
    # tương ứng với 7 thuộc tính được sử dụng
    # trong dữ liệu ẩn danh
    original_feature_columns = [
        "tuoi",
        "loai_cong_viec",
        "so_nam_hoc",
        "tinh_trang_hon_nhan",
        "nghe_nghiep",
        "gio_lam_moi_tuan",
        "quoc_gia"
    ]


    # Chỉ lấy 7 feature cần thiết cho Machine Learning
    # Không đưa cột target thu_nhap vào X
    original_features = (
        dataframe[
            original_feature_columns
        ]
        .copy()
    )


    # Chuyển ký hiệu ? thành np.nan
    # để SimpleImputer có thể xử lý ở bước preprocessing
    #
    # Không xóa các bản ghi có dữ liệu bị thiếu
    original_features = (
        original_features
        .replace(
            "?",
            np.nan
        )
    )


    # Lấy riêng cột target thu_nhap
    # Đây là nhãn mà mô hình cần dự đoán
    target = (
        dataframe[
            target_column
        ]
        .copy()
    )


    # Trả về:
    # original_features = X
    # target = y
    return (
        original_features,
        target
    )


# HÀM 5:
# CHUẨN BỊ FEATURE VÀ TARGET CỦA DỮ LIỆU ẨN DANH


# Tạo hàm prepare_anonymized_features_target()
# để tách dữ liệu ẩn danh thành:
# - X = các feature đã được tổng quát hóa
# - y = target thu_nhap
def prepare_anonymized_features_target(
    dataframe,
    target_column="thu_nhap"
):

    # Lấy danh sách tất cả các cột
    # ngoại trừ cột target thu_nhap
    #
    # Cách này giúp hàm dùng được cho cả:
    # Strategy 1 có tuoi_nhom_3
    # Strategy 2 có tuoi_nhom_high
    anonymized_feature_columns = [
        column
        for column in dataframe.columns
        if column != target_column
    ]


    # Lấy các feature của dữ liệu đã ẩn danh
    # và tạo một bản sao để tránh sửa trực tiếp DataFrame ban đầu
    anonymized_features = (
        dataframe[
            anonymized_feature_columns
        ]
        .copy()
    )


    # Lấy riêng cột target thu_nhap
    # Target này không bị thay đổi trong quá trình ẩn danh hóa
    target = (
        dataframe[
            target_column
        ]
        .copy()
    )


    # Trả về:
    # anonymized_features = X của dữ liệu ẩn danh
    # target = y dùng để huấn luyện và đánh giá mô hình
    return (
        anonymized_features,
        target
    )


# ============================================================
# HÀM 6:
# TẠO BỘ TIỀN XỬ LÝ CHO DỮ LIỆU ORIGINAL
# ============================================================


# Tạo hàm build_original_preprocessor()
# để xử lý riêng:
# - các cột dạng số
# - các cột dạng phân loại
def build_original_preprocessor():

    # Khai báo 3 feature dạng số
    # Đây là các cột sẽ được điền missing bằng median
    # và sau đó được chuẩn hóa bằng StandardScaler
    numeric_features = [
        "tuoi",
        "so_nam_hoc",
        "gio_lam_moi_tuan"
    ]


    # Khai báo 4 feature dạng phân loại
    # Đây là các cột sẽ được điền missing
    # và chuyển sang dạng số bằng OneHotEncoder
    categorical_features = [
        "loai_cong_viec",
        "tinh_trang_hon_nhan",
        "nghe_nghiep",
        "quoc_gia"
    ]


    # PIPELINE XỬ LÝ CỘT SỐ


    # Tạo pipeline dành cho các feature dạng số
    numeric_pipeline = Pipeline(
        steps=[

            # Nếu cột số có missing value
            # thì điền bằng giá trị trung vị của tập Train
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            ),

            # Chuẩn hóa các feature số
            # để Logistic Regression học ổn định hơn
            (
                "scaler",
                StandardScaler()
            )
        ]
    )


    # PIPELINE XỬ LÝ CỘT PHÂN LOẠI


    # Tạo pipeline dành cho các feature dạng phân loại
    categorical_pipeline = Pipeline(
        steps=[

            # Điền missing value bằng giá trị xuất hiện nhiều nhất
            # Việc tính giá trị này sau này chỉ được fit trên tập Train
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            # Chuyển các giá trị phân loại thành các cột 0/1
            # handle_unknown="ignore" giúp Validation/Test
            # không bị lỗi nếu xuất hiện giá trị chưa có trong Train
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )


    # GHÉP HAI LOẠI TIỀN XỬ LÝ


    # ColumnTransformer giúp áp dụng:
    # numeric_pipeline cho các cột số
    # categorical_pipeline cho các cột phân loại
    original_preprocessor = ColumnTransformer(
        transformers=[

            # Áp dụng pipeline số cho 3 feature số
            (
                "numeric",
                numeric_pipeline,
                numeric_features
            ),

            # Áp dụng pipeline phân loại cho 4 feature categorical
            (
                "categorical",
                categorical_pipeline,
                categorical_features
            )
        ]
    )


    # Trả về bộ tiền xử lý hoàn chỉnh
    # nhưng CHƯA fit vào dữ liệu ở bước này
    return original_preprocessor


# TẠO BỘ TIỀN XỬ LÝ CHO DỮ LIỆU ANONYMIZED


# Tạo hàm build_anonymized_preprocessor()
# để xử lý các feature đã được ẩn danh hóa
#
# Các feature sau generalization đều đang ở dạng phân loại
# nên chúng ta sẽ:
# - xử lý missing value
# - chuyển toàn bộ thành dạng số bằng OneHotEncoder
def build_anonymized_preprocessor(
    anonymized_feature_columns
):

    # Tạo pipeline xử lý các feature ẩn danh
    anonymized_pipeline = Pipeline(
        steps=[

            # Nếu xuất hiện missing value
            # thì điền bằng giá trị xuất hiện nhiều nhất trong tập Train
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            # Chuyển các giá trị phân loại thành các cột 0/1
            # handle_unknown="ignore" giúp Validation/Test
            # không bị lỗi nếu gặp category chưa xuất hiện trong Train
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )


    # Dùng ColumnTransformer để áp dụng
    # pipeline trên cho toàn bộ các feature ẩn danh
    anonymized_preprocessor = ColumnTransformer(
        transformers=[

            # Áp dụng cùng một pipeline
            # cho tất cả feature của dữ liệu ẩn danh
            (
                "categorical",
                anonymized_pipeline,
                anonymized_feature_columns
            )
        ]
    )


    # Trả về bộ preprocessing hoàn chỉnh
    # nhưng chưa fit dữ liệu ở bước này
    return anonymized_preprocessor


# TẠO PIPELINE LOGISTIC REGRESSION


# Tạo hàm build_logistic_regression_pipeline()
# để ghép:
# - bộ preprocessing
# - mô hình Logistic Regression
#
# Thành một quy trình Machine Learning thống nhất
def build_logistic_regression_pipeline(
    preprocessor
):

    # Tạo pipeline Machine Learning
    # Dữ liệu sẽ đi qua preprocessing trước
    # rồi mới được đưa vào Logistic Regression
    model_pipeline = Pipeline(
        steps=[

            # Bước 1:
            # Tiền xử lý dữ liệu
            (
                "preprocessor",
                preprocessor
            ),

            # Bước 2:
            # Huấn luyện mô hình Logistic Regression
            (
                "model",
                LogisticRegression(

                    # Tăng số vòng lặp tối đa
                    # để mô hình có đủ thời gian hội tụ
                    max_iter=1000,

                    # Cố định random_state
                    # để hỗ trợ khả năng tái lập thí nghiệm
                    random_state=42
                )
            )
        ]
    )


    # Trả về pipeline hoàn chỉnh
    # nhưng CHƯA huấn luyện mô hình ở bước này
    return model_pipeline

# TỰ ĐỘNG ĐÁNH GIÁ UTILITY TRÊN VALIDATION
# CHO MỘT STRATEGY ẨN DANH


# Tạo hàm evaluate_strategy_validation()
# để tự động thực hiện toàn bộ quy trình:
#
# 1. Căn chỉnh dữ liệu Original
# 2. Chia Train / Validation / Test
# 3. Chuẩn bị feature và target
# 4. Tạo preprocessing
# 5. Huấn luyện Logistic Regression
# 6. Dự đoán trên Validation
# 7. Tính các metric
# 8. Tính Utility Retention và Utility Score
def evaluate_strategy_validation(
    original_dataframe,
    anonymized_dataframe,
    retained_indices,
    target_column="thu_nhap",
    random_state=42
):


    # BƯỚC 1:
    # CĂN CHỈNH DỮ LIỆU ORIGINAL


    # Lấy đúng các bản ghi Original
    # còn tồn tại trong dữ liệu ẩn danh
    aligned_original_data = (
        get_aligned_original_data(
            original_dataframe,
            retained_indices
        )
    )


    # BƯỚC 2:
    # KIỂM TRA ORIGINAL VÀ ANONYMIZED CÓ KHỚP KHÔNG


    # Kiểm tra index của hai bộ dữ liệu
    # phải giống nhau hoàn toàn
    same_indices = (
        aligned_original_data.index.tolist()
        ==
        anonymized_dataframe.index.tolist()
    )


    # Nếu index không giống nhau
    # thì dừng để tránh đánh giá sai các bản ghi
    if not same_indices:
        raise ValueError(
            "Index của Original và Anonymized không khớp."
        )


    # Kiểm tra target thu_nhap của hai bộ dữ liệu
    # phải giống nhau từng bản ghi
    same_target = (
        aligned_original_data[target_column].tolist()
        ==
        anonymized_dataframe[target_column].tolist()
    )


    # Nếu target không giống nhau
    # thì dừng vì không thể so sánh hai mô hình công bằng
    if not same_target:
        raise ValueError(
            "Target của Original và Anonymized không khớp."
        )


    # BƯỚC 3:
    # CHIA TRAIN / VALIDATION / TEST


    # Chia index theo đúng tỷ lệ:
    # 60% Train
    # 20% Validation
    # 20% Test
    train_indices, validation_indices, test_indices = (
        split_train_validation_test_indices(
            aligned_original_data,
            target_column=target_column,
            random_state=random_state
        )
    )


    # BƯỚC 4:
    # LẤY TRAIN / VALIDATION CỦA ORIGINAL


    # Lấy các tập dữ liệu Original
    original_train, original_validation, original_test = (
        get_data_splits_by_indices(
            aligned_original_data,
            train_indices,
            validation_indices,
            test_indices
        )
    )


    # BƯỚC 5:
    # LẤY TRAIN / VALIDATION CỦA ANONYMIZED


    # Lấy các tập dữ liệu Anonymized
    # bằng chính xác cùng bộ index với Original
    anonymized_train, anonymized_validation, anonymized_test = (
        get_data_splits_by_indices(
            anonymized_dataframe,
            train_indices,
            validation_indices,
            test_indices
        )
    )



    # BƯỚC 6:
    # CHUẨN BỊ X VÀ y CỦA ORIGINAL


    # Tách feature và target của Original Train
    X_original_train, y_original_train = (
        prepare_original_features_target(
            original_train,
            target_column=target_column
        )
    )


    # Tách feature và target của Original Validation
    X_original_validation, y_original_validation = (
        prepare_original_features_target(
            original_validation,
            target_column=target_column
        )
    )


    # BƯỚC 7:
    # CHUẨN BỊ X VÀ y CỦA ANONYMIZED


    # Tách feature và target của Anonymized Train
    X_anonymized_train, y_anonymized_train = (
        prepare_anonymized_features_target(
            anonymized_train,
            target_column=target_column
        )
    )


    # Tách feature và target của Anonymized Validation
    X_anonymized_validation, y_anonymized_validation = (
        prepare_anonymized_features_target(
            anonymized_validation,
            target_column=target_column
        )
    )


    # BƯỚC 8:
    # TẠO MÔ HÌNH ORIGINAL


    # Tạo preprocessing mới cho Original
    original_preprocessor = (
        build_original_preprocessor()
    )


    # Tạo Pipeline Logistic Regression cho Original
    original_model_pipeline = (
        build_logistic_regression_pipeline(
            original_preprocessor
        )
    )



    # BƯỚC 9:
    # HUẤN LUYỆN MÔ HÌNH ORIGINAL


    # Huấn luyện Original chỉ trên tập Train
    original_model_pipeline.fit(
        X_original_train,
        y_original_train
    )


    # BƯỚC 10:
    # TẠO MÔ HÌNH ANONYMIZED


    # Lấy danh sách feature của dữ liệu ẩn danh
    anonymized_feature_columns = (
        X_anonymized_train
        .columns
        .tolist()
    )


    # Tạo preprocessing cho dữ liệu ẩn danh
    anonymized_preprocessor = (
        build_anonymized_preprocessor(
            anonymized_feature_columns
        )
    )


    # Tạo Pipeline Logistic Regression
    # dành cho dữ liệu Anonymized
    anonymized_model_pipeline = (
        build_logistic_regression_pipeline(
            anonymized_preprocessor
        )
    )


    # BƯỚC 11:
    # HUẤN LUYỆN MÔ HÌNH ANONYMIZED


    # Huấn luyện mô hình trên Anonymized Train
    anonymized_model_pipeline.fit(
        X_anonymized_train,
        y_anonymized_train
    )


    # BƯỚC 12:
    # DỰ ĐOÁN ORIGINAL VALIDATION


    # Dự đoán nhãn trên Original Validation
    y_pred_original = (
        original_model_pipeline.predict(
            X_original_validation
        )
    )


    # Lấy danh sách các lớp của mô hình Original
    original_classes = (
        original_model_pipeline
        .named_steps["model"]
        .classes_
    )


    # Tìm vị trí của lớp dương >50K
    original_positive_index = (
        list(
            original_classes
        )
        .index(
            ">50K"
        )
    )


    # Lấy xác suất thuộc lớp >50K
    # để tính ROC-AUC
    y_prob_original = (
        original_model_pipeline.predict_proba(
            X_original_validation
        )[
            :,
            original_positive_index
        ]
    )


    # BƯỚC 13:
    # DỰ ĐOÁN ANONYMIZED VALIDATION


    # Dự đoán nhãn trên Anonymized Validation
    y_pred_anonymized = (
        anonymized_model_pipeline.predict(
            X_anonymized_validation
        )
    )


    # Lấy danh sách các lớp của mô hình Anonymized
    anonymized_classes = (
        anonymized_model_pipeline
        .named_steps["model"]
        .classes_
    )


    # Tìm vị trí của lớp dương >50K
    anonymized_positive_index = (
        list(
            anonymized_classes
        )
        .index(
            ">50K"
        )
    )


    # Lấy xác suất thuộc lớp >50K
    y_prob_anonymized = (
        anonymized_model_pipeline.predict_proba(
            X_anonymized_validation
        )[
            :,
            anonymized_positive_index
        ]
    )


    # BƯỚC 14:
    # TÍNH METRIC ORIGINAL


    # Tính Accuracy, Precision, Recall,
    # F1-score, Balanced Accuracy và ROC-AUC
    original_metrics = (
        utility_evaluator.evaluate_classification_metrics(
            y_true=y_original_validation,
            y_pred=y_pred_original,
            y_prob=y_prob_original,
            positive_label=">50K"
        )
    )


    # BƯỚC 15:
    # TÍNH METRIC ANONYMIZED

    # Tính các metric tương ứng
    # cho mô hình học trên dữ liệu ẩn danh
    anonymized_metrics = (
        utility_evaluator.evaluate_classification_metrics(
            y_true=y_anonymized_validation,
            y_pred=y_pred_anonymized,
            y_prob=y_prob_anonymized,
            positive_label=">50K"
        )
    )


    # BƯỚC 16:
    # TÍNH UTILITY RETENTION VÀ UTILITY SCORE

    # So sánh Original và Anonymized
    # để tính mức độ giữ lại hiệu quả Machine Learning
    utility_result = (
        utility_evaluator.calculate_utility_retention(
            original_metrics=original_metrics,
            anonymized_metrics=anonymized_metrics
        )
    )

    # BƯỚC 17:
    # TRẢ VỀ TOÀN BỘ KẾT QUẢ CẦN THIẾT

    # Trả về dictionary để notebook
    # có thể lấy từng kết quả theo tên
    return {

        # Metric của Original trên Validation
        "original_metrics": original_metrics,

        # Metric của Anonymized trên Validation
        "anonymized_metrics": anonymized_metrics,

        # Utility Retention và Utility Score
        "utility_result": utility_result,

        # Utility Score riêng để tiện dùng khi xếp hạng Strategy
        "utility_score_percent": utility_result[
            "utility_score_%"
        ],

        # Giữ lại bộ index Train
        "train_indices": train_indices,

        # Giữ lại bộ index Validation
        "validation_indices": validation_indices,

        # Giữ lại bộ index Test
        # Test CHƯA được dùng để đánh giá ở hàm này
        "test_indices": test_indices,

        # Giữ lại mô hình Original đã train
        # để có thể kiểm tra sau nếu cần
        "original_model_pipeline": original_model_pipeline,

        # Giữ lại mô hình Anonymized đã train
        "anonymized_model_pipeline": anonymized_model_pipeline
    }
# ĐÁNH GIÁ STRATEGY ĐƯỢC CHỌN TRÊN TẬP TEST CUỐI CÙNG
def evaluate_selected_strategy_test(
    original_dataframe,
    anonymized_dataframe,
    retained_indices,
    validation_result,
    target_column="thu_nhap"
):
    """
    Đánh giá Strategy đã được chọn trên tập Test cuối cùng.

    Lưu ý:
    - Strategy đã phải được chọn trước bằng Validation.
    - Test chỉ được sử dụng sau khi đã chọn Strategy tốt nhất.
    - Hàm sử dụng lại các mô hình đã huấn luyện trên Train.
    """

    # 1. CĂN CHỈNH DỮ LIỆU ORIGINAL
    # Chỉ giữ những bản ghi Original
    # tương ứng với dữ liệu còn lại sau Suppression
    original_aligned = get_aligned_original_data(
        original_dataframe=original_dataframe,
        retained_indices=retained_indices
    )

    # 2. LẤY INDEX TEST ĐÃ ĐƯỢC GIỮ RIÊNG
    # Không chia dữ liệu lại lần nữa
    # mà sử dụng đúng Test index đã tạo trong Validation
    test_indices = validation_result[
        "test_indices"
    ]


    # 3. TẠO ORIGINAL TEST VÀ ANONYMIZED TEST

    # Lấy tập Test của dữ liệu gốc
    original_test = (
        original_aligned
        .loc[
            test_indices
        ]
        .copy()
    )


    # Lấy tập Test của dữ liệu đã ẩn danh
    anonymized_test = (
        anonymized_dataframe
        .loc[
            test_indices
        ]
        .copy()
    )


    # 4. KIỂM TRA INDEX

    # Hai tập Test phải chứa đúng cùng các bản ghi
    same_test_indices = (
        original_test.index.tolist()
        ==
        anonymized_test.index.tolist()
    )


    # Nếu index không giống nhau
    # thì dừng ngay để tránh đánh giá sai
    if not same_test_indices:
        raise ValueError(
            "Original Test và Anonymized Test không cùng index."
        )


    # 5. KIỂM TRA TARGET

    # Target của Original và Anonymized
    # phải giống nhau hoàn toàn
    same_test_target = (
        original_test[
            target_column
        ].tolist()
        ==
        anonymized_test[
            target_column
        ].tolist()
    )


    # Nếu target không giống nhau
    # thì không được tiếp tục đánh giá
    if not same_test_target:
        raise ValueError(
            "Target của Original Test và Anonymized Test không giống nhau."
        )


    # 6. CHUẨN BỊ FEATURE VÀ TARGET ORIGINAL

    # Tách 7 feature gốc và target
    X_original_test, y_original_test = (
        prepare_original_features_target(
            original_test,
            target_column=target_column
        )
    )


    # 7. CHUẨN BỊ FEATURE VÀ TARGET ANONYMIZED

    # Tách feature đã ẩn danh và target
    X_anonymized_test, y_anonymized_test = (
        prepare_anonymized_features_target(
            anonymized_test,
            target_column=target_column
        )
    )


    # 8. LẤY HAI MÔ HÌNH ĐÃ HUẤN LUYỆN

    # Lấy mô hình Original đã học trên Train
    original_model = validation_result[
        "original_model_pipeline"
    ]


    # Lấy mô hình Anonymized đã học trên Train
    anonymized_model = validation_result[
        "anonymized_model_pipeline"
    ]


    # 9. DỰ ĐOÁN ORIGINAL TEST

    # Dự đoán nhãn
    y_pred_original = original_model.predict(
        X_original_test
    )


    # Lấy danh sách class của mô hình
    original_classes = (
        original_model
        .named_steps["model"]
        .classes_
    )


    # Tìm vị trí của lớp dương >50K
    original_positive_index = (
        list(
            original_classes
        )
        .index(
            ">50K"
        )
    )


    # Lấy xác suất dự đoán lớp >50K
    y_prob_original = (
        original_model.predict_proba(
            X_original_test
        )[
            :,
            original_positive_index
        ]
    )


    # 10. DỰ ĐOÁN ANONYMIZED TEST

    # Dự đoán nhãn
    y_pred_anonymized = anonymized_model.predict(
        X_anonymized_test
    )


    # Lấy danh sách class của mô hình
    anonymized_classes = (
        anonymized_model
        .named_steps["model"]
        .classes_
    )


    # Tìm vị trí của lớp dương >50K
    anonymized_positive_index = (
        list(
            anonymized_classes
        )
        .index(
            ">50K"
        )
    )


    # Lấy xác suất dự đoán lớp >50K
    y_prob_anonymized = (
        anonymized_model.predict_proba(
            X_anonymized_test
        )[
            :,
            anonymized_positive_index
        ]
    )


    # 11. TÍNH METRIC ORIGINAL TEST

    original_metrics = (
        utility_evaluator.evaluate_classification_metrics(
            y_true=y_original_test,
            y_pred=y_pred_original,
            y_prob=y_prob_original,
            positive_label=">50K"
        )
    )


    # 12. TÍNH METRIC ANONYMIZED TEST


    anonymized_metrics = (
        utility_evaluator.evaluate_classification_metrics(
            y_true=y_anonymized_test,
            y_pred=y_pred_anonymized,
            y_prob=y_prob_anonymized,
            positive_label=">50K"
        )
    )


    # 13. TÍNH UTILITY RETENTION CUỐI CÙNG

    utility_result = (
        utility_evaluator.calculate_utility_retention(
            original_metrics=original_metrics,
            anonymized_metrics=anonymized_metrics
        )
    )


    # 14. TRẢ VỀ TOÀN BỘ KẾT QUẢ

    return {

        # Số lượng bản ghi Test
        "test_size": len(
            test_indices
        ),

        # Bộ index Test
        "test_indices": test_indices,

        # Metric của dữ liệu Original
        "original_metrics": original_metrics,

        # Metric của dữ liệu Anonymized
        "anonymized_metrics": anonymized_metrics,

        # Kết quả Utility Retention
        "utility_result": utility_result,

        # Final Utility Score
        "utility_score_percent": (
            utility_result[
                "utility_score_%"
            ]

        ),

        # Kết quả kiểm tra index
        "same_test_indices": same_test_indices,

        # Kết quả kiểm tra target
        "same_test_target": same_test_target
    }