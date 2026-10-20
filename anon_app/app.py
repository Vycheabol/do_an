
# 1. IMPORT THƯ VIỆN CƠ BẢN

# Path dùng để xử lý đường dẫn thư mục và file.
#
# Ví dụ trong project này:
# Path(__file__) giúp Python xác định
# vị trí thực tế của file app.py.
from pathlib import Path

# sys dùng để thêm thư mục src vào Python path,
# giúp app.py import được các module backend.
import sys

# pandas dùng để đọc file CSV và xử lý DataFrame.
import pandas as pd

# matplotlib.pyplot dùng để vẽ biểu đồ
# Data Retention - Utility.
import matplotlib.pyplot as plt

# streamlit dùng để tạo giao diện web.
import streamlit as st



# 2. XÁC ĐỊNH THƯ MỤC GỐC CỦA PROJECT

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


# 3. XÁC ĐỊNH THƯ MỤC SRC


SRC_DIR = (
    PROJECT_ROOT
    / "src"
)


# Nếu src chưa có trong sys.path,
# ta thêm vào đầu danh sách.
if str(SRC_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(SRC_DIR)
    )



# 4. IMPORT CÁC MODULE BACKEND CỦA ĐỒ ÁN

# Module sinh tự động 4 Candidate.
import strategy_generator

# Module thực hiện Generalization + Suppression.
import anonymization_engine

# Module đánh giá k-anonymity và l-diversity.
import privacy_analyzer

# Module đánh giá Utility bằng Logistic Regression.
import ml_evaluator

# Module xếp hạng và lựa chọn Candidate tốt nhất.
import strategy_selector



# 5. CẤU HÌNH GIAO DIỆN STREAMLIT

# set_page_config() nên được gọi trước
# các lệnh hiển thị khác của Streamlit.
st.set_page_config(
    page_title="Hệ thống ẩn danh hóa dữ liệu",
    page_icon="🔐",
    layout="wide"
)


# 6. TIÊU ĐỀ HỆ THỐNG

st.title(
    "🔐 Hệ thống ẩn danh hóa dữ liệu thông minh"
)


st.subheader(
    "Hỗ trợ bảo vệ dữ liệu theo hướng Privacy-Preserving "
    "và đánh giá Utility bằng Machine Learning"
)


# Hiển thị lưu ý khoa học cho người dùng.
st.info(
    "Hệ thống sử dụng k-anonymity và l-diversity "
    "làm tiêu chí kỹ thuật trong thực nghiệm. "
    "Việc đạt các ngưỡng này không đồng nghĩa "
    "tự động bảo đảm toàn bộ yêu cầu của GDPR."
)



# 7. PHẦN UPLOAD DATASET

st.header(
    "1. Tải dữ liệu"
)


# Chỉ cho phép người dùng upload file CSV.
uploaded_file = st.file_uploader(
    "Chọn dataset định dạng CSV",
    type=[
        "csv"
    ]
)


# 8. TRƯỜNG HỢP CHƯA UPLOAD FILE

if uploaded_file is None:

    # Nếu chưa có file thì chỉ hiển thị cảnh báo.
    st.warning(
        "Vui lòng tải một file CSV để bắt đầu."
    )


# 9. TRƯỜNG HỢP ĐÃ UPLOAD FILE

else:

    try:

        # 9.1. ĐỌC DATASET


        # sep=None yêu cầu pandas tự nhận diện delimiter.
        # engine="python" được dùng vì chức năng
        # tự nhận diện dấu phân cách cần Python parser.
        # Nhờ vậy app có thể đọc được cả file CSV
        # dùng dấu "," và file CSV dùng dấu ";".
        data = pd.read_csv(
            uploaded_file,
            sep=None,
            engine="python"
        )


        # Không cho phép dataset rỗng.
        if len(data) == 0:

            raise ValueError(
                "Dataset không có bản ghi."
            )


        st.success(
            "Đọc dataset thành công."
        )


        # 10. HIỂN THỊ THÔNG TIN DATASET

        st.header(
            "2. Thông tin dataset"
        )


        # Chia giao diện thành 3 cột.
        column_1, column_2, column_3 = (
            st.columns(
                3
            )
        )


        # Hiển thị số bản ghi

        with column_1:

            st.metric(
                label="Số bản ghi",
                value=len(
                    data
                )
            )


        # Hiển thị số cột

        with column_2:

            st.metric(
                label="Số cột",
                value=len(
                    data.columns
                )
            )


        # Kiểm tra cột thu_nhap

        # thu_nhap vừa là target của ML,
        # vừa là sensitive attribute cho l-diversity.
        target_exists = (
            "thu_nhap"
            in data.columns
        )


        with column_3:

            st.metric(
                label="Có cột thu_nhap?",
                value=(
                    "Có"
                    if target_exists
                    else "Không"
                )
            )


        if target_exists:

            st.success(
                "Dataset có cột target/sensitive 'thu_nhap'."
            )

        else:

            st.error(
                "Dataset không có cột 'thu_nhap'."
            )


        # 10.1. HIỂN THỊ DANH SÁCH CỘT

        st.subheader(
            "Danh sách các cột"
        )


        st.write(
            data.columns.tolist()
        )


        # 10.2. XEM TRƯỚC DỮ LIỆU

        st.subheader(
            "Xem trước dữ liệu"
        )


        # Chỉ hiển thị 20 dòng đầu để giao diện gọn.
        st.dataframe(
            data.head(
                20
            ),
            width="stretch"
        )


        # 10.3. KIỂM TRA GIÁ TRỊ THIẾU

        st.subheader(
            "Kiểm tra giá trị thiếu"
        )


        # isna().sum() đếm số NaN trong từng cột.
        missing_values = (
            data
            .isna()
            .sum()
            .reset_index()
        )


        # Đổi tên cột để hiển thị dễ hiểu.
        missing_values.columns = [
            "Tên cột",
            "Số giá trị thiếu"
        ]


        st.dataframe(
            missing_values,
            width="stretch"
        )


        # 11. KIỂM TRA CẤU TRÚC DATASET


        st.header(
            "3. Kiểm tra cấu trúc dữ liệu"
        )


        # Đây là các cột tối thiểu
        # mà pipeline hiện tại cần sử dụng.
        required_columns = [
            "tuoi",
            "loai_cong_viec",
            "so_nam_hoc",
            "tinh_trang_hon_nhan",
            "nghe_nghiep",
            "gio_lam_moi_tuan",
            "quoc_gia",
            "thu_nhap"
        ]


        # Tìm các cột bắt buộc nhưng bị thiếu.
        missing_required_columns = [
            column
            for column in required_columns
            if column not in data.columns
        ]


        # Nếu không thiếu cột nào:
        # dataset đủ điều kiện chạy.
        if len(
            missing_required_columns
        ) == 0:

            dataset_valid = True

            st.success(
                "Dataset có đầy đủ các cột cần thiết cho hệ thống."
            )


        # Nếu thiếu cột:
        # khóa nút chạy ẩn danh hóa.
        else:

            dataset_valid = False

            st.error(
                "Dataset đang thiếu các cột bắt buộc:"
            )

            st.write(
                missing_required_columns
            )


        # ====================================================
        # 12. CẤU HÌNH PRIVACY
        # ====================================================

        st.header(
            "4. Cấu hình ẩn danh hóa"
        )


        config_column_1, config_column_2 = (
            st.columns(
                2
            )
        )


        # 12.1. k-anonymity

        with config_column_1:

            # Mặc định k=5.
            #
            # Nghĩa là sau ẩn danh hóa,
            # mỗi equivalence class phải có ít nhất 5 bản ghi.
            k_required = st.number_input(
                label="Giá trị k-anonymity",
                min_value=1,
                max_value=20,
                value=5,
                step=1
            )


        # 12.2. l-diversity

        with config_column_2:

            # thu_nhap hiện có 2 lớp:
            # <=50K và >50K.
            #
            # Vì vậy l tối đa hợp lý hiện tại là 2.
            l_required = st.number_input(
                label="Giá trị l-diversity",
                min_value=1,
                max_value=2,
                value=2,
                step=1
            )


        st.info(
            "Trong đồ án hiện tại, k=5 và l=2 "
            "là các ngưỡng thực nghiệm được lựa chọn. "
            "Đây không phải ngưỡng bắt buộc của GDPR."
        )


        st.write(
            f"Cấu hình hiện tại: "
            f"k = {k_required}, "
            f"l = {l_required}"
        )


        # 13. NÚT BẮT ĐẦU XỬ LÝ

        start_button = st.button(
            "🔐 Bắt đầu ẩn danh hóa",
            type="primary",
            disabled=not dataset_valid,
            width="stretch"
        )


        # 14. CHẠY HỆ THỐNG


        if start_button:

            # XÓA KẾT QUẢ CŨ TRƯỚC KHI CHẠY LẦN MỚI
            # Streamlit giữ session_state qua các lần rerun.
            # Nếu lần chạy mới lỗi giữa chừng mà không xóa
            # kết quả cũ, giao diện có thể hiển thị nhầm output cũ.
            old_result_keys = [
                "candidate_results",
                "ranking_dataframe",
                "selected_candidate",
                "selected_strategy_name",
                "selected_release_data",
                "final_test_result",
                "run_file_name",
                "run_k_required",
                "run_l_required",
                "run_row_count"
            ]


            for state_key in old_result_keys:

                st.session_state.pop(
                    state_key,
                    None
                )


            st.success(
                f"Đã nhận cấu hình "
                f"k={k_required}, "
                f"l={l_required}."
            )


            # Spinner giúp người dùng biết
            # hệ thống đang chạy xử lý.
            with st.spinner(
                "Hệ thống đang xử lý dữ liệu..."
            ):


                # 14.1. SINH 4 CANDIDATE

                # Candidate được sinh từ tổ hợp:
                #
                # 2 mức Age:
                # - age3
                # - age_high
                #
                # 2 mức Hours:
                # - hours3
                # - hours2
                #
                # Tổng:
                # 2 x 2 = 4 Candidate.
                candidate_strategies = (
                    strategy_generator
                    .generate_candidate_strategies()
                )


                # Kiểm tra cấu hình Candidate.
                candidates_valid = (
                    strategy_generator
                    .validate_candidate_strategies(
                        candidate_strategies
                    )
                )


                if candidates_valid is False:

                    raise ValueError(
                        "Danh sách Candidate không hợp lệ."
                    )


                # Dictionary trung tâm lưu toàn bộ
                # kết quả của từng Candidate.
                candidate_results = {}


                # Danh sách này dùng để tạo bảng hiển thị
                # kết quả Anonymization.
                anonymization_rows = []


                # 14.2. CHẠY ANONYMIZATION CHO TỪNG CANDIDATE


                for candidate in candidate_strategies:

                    # Lấy tên Candidate.
                    strategy_name = (
                        candidate[
                            "strategy_name"
                        ]
                    )


                    # Chạy toàn bộ:
                    #
                    # Generalization
                    #     ↓
                    # k-anonymity Suppression
                    #     ↓
                    # l-diversity Suppression
                    #
                    # release_data:
                    # dataset đã ẩn danh
                    #
                    # retained_indices:
                    # index gốc của các bản ghi còn lại.
                    release_data, retained_indices = (
                        anonymization_engine
                        .anonymize_candidate_strategy(
                            dataframe=data,
                            strategy_config=candidate,
                            k_required=int(
                                k_required
                            ),
                            l_required=int(
                                l_required
                            )
                        )
                    )


                    # release_data và retained_indices
                    # bắt buộc phải có cùng số phần tử.
                    if (
                        len(
                            release_data
                        )
                        !=
                        len(
                            retained_indices
                        )
                    ):

                        raise ValueError(
                            f"{strategy_name}: "
                            "release_data và retained_indices "
                            "không khớp."
                        )


                    # Tính số bản ghi bị Suppression
                    suppressed_records = (
                        len(
                            data
                        )
                        -
                        len(
                            release_data
                        )
                    )


                    # Tính tỷ lệ Suppression

                    suppression_percent = (
                        suppressed_records
                        /
                        len(
                            data
                        )
                        *
                        100
                    )


                    # Tính Data Retention

                    # Data Retention là tỷ lệ dữ liệu
                    # vẫn còn lại sau ẩn danh hóa.
                    data_retention_percent = (
                        len(
                            release_data
                        )
                        /
                        len(
                            data
                        )
                        *
                        100
                    )


                    # Lưu toàn bộ kết quả Candidate
                    # vào dictionary trung tâm.
                    candidate_results[
                        strategy_name
                    ] = {

                        "config":
                            candidate,

                        "release_data":
                            release_data,

                        "retained_indices":
                            retained_indices,

                        "suppressed_records":
                            suppressed_records,

                        "suppression_percent":
                            suppression_percent,

                        "data_retention_percent":
                            data_retention_percent
                    }


                    # Thêm một dòng cho bảng giao diện.
                    anonymization_rows.append(
                        {

                            "Candidate":
                                strategy_name,

                            "Age Level":
                                candidate[
                                    "age_level"
                                ],

                            "Hours Level":
                                candidate[
                                    "hours_level"
                                ],

                            "Bản ghi gốc":
                                len(
                                    data
                                ),

                            "Bản ghi sau ẩn danh":
                                len(
                                    release_data
                                ),

                            "Suppressed":
                                suppressed_records,

                            "Suppression (%)":
                                round(
                                    suppression_percent,
                                    2
                                ),

                            "Data Retention (%)":
                                round(
                                    data_retention_percent,
                                    2
                                )
                        }
                    )


                # 15. HIỂN THỊ KẾT QUẢ ANONYMIZATION

                st.success(
                    f"Đã chạy thành công "
                    f"{len(candidate_strategies)} Candidate."
                )


                st.header(
                    "5. Kết quả ẩn danh hóa của các Candidate"
                )


                anonymization_dataframe = (
                    pd.DataFrame(
                        anonymization_rows
                    )
                )


                st.dataframe(
                    anonymization_dataframe,
                    width="stretch",
                    hide_index=True
                )


                # 16. PRIVACY EVALUATION

                privacy_rows = []


                for candidate in candidate_strategies:

                    strategy_name = (
                        candidate[
                            "strategy_name"
                        ]
                    )


                    # Lấy dataset ẩn danh của Candidate.
                    release_data = (
                        candidate_results[
                            strategy_name
                        ][
                            "release_data"
                        ]
                    )


                    # Mỗi Candidate có QI khác nhau
                    # ở cột Age và Hours.
                    qi_columns = (
                        anonymization_engine
                        .get_candidate_qi_columns(
                            candidate
                        )
                    )


                    # Kiểm tra lại:
                    # - k_min
                    # - k_valid
                    # - l_min
                    # - l_valid
                    # - privacy_valid
                    privacy_result = (
                        privacy_analyzer
                        .evaluate_privacy_full(
                            dataframe=release_data,
                            qi_columns=qi_columns,
                            sensitive_column="thu_nhap",
                            k_required=int(
                                k_required
                            ),
                            l_required=int(
                                l_required
                            )
                        )
                    )


                    # Lưu kết quả Privacy.
                    candidate_results[
                        strategy_name
                    ][
                        "privacy"
                    ] = privacy_result


                    # Tạo dòng cho bảng giao diện.
                    privacy_rows.append(
                        {

                            "Candidate":
                                strategy_name,

                            "k_min":
                                privacy_result[
                                    "k_min"
                                ],

                            "k_required":
                                privacy_result[
                                    "k_required"
                                ],

                            "k_valid":
                                privacy_result[
                                    "k_valid"
                                ],

                            "Vi phạm k":
                                privacy_result[
                                    "so_ban_ghi_vi_pham_k"
                                ],

                            "l_min":
                                privacy_result[
                                    "l_min"
                                ],

                            "l_required":
                                privacy_result[
                                    "l_required"
                                ],

                            "l_valid":
                                privacy_result[
                                    "l_valid"
                                ],

                            "Nhóm vi phạm l":
                                privacy_result[
                                    "so_nhom_vi_pham_l"
                                ],

                            "Bản ghi vi phạm l":
                                privacy_result[
                                    "so_ban_ghi_vi_pham_l"
                                ],

                            "Privacy valid":
                                privacy_result[
                                    "privacy_valid"
                                ]
                        }
                    )

                # 17. HIỂN THỊ PRIVACY

                st.header(
                    "6. Đánh giá Privacy của các Candidate"
                )


                privacy_dataframe = (
                    pd.DataFrame(
                        privacy_rows
                    )
                )


                st.dataframe(
                    privacy_dataframe,
                    width="stretch",
                    hide_index=True
                )


                # Đếm số Candidate đạt privacy_valid=True.
                valid_privacy_count = sum(
                    1
                    for strategy_name
                    in candidate_results
                    if candidate_results[
                        strategy_name
                    ][
                        "privacy"
                    ][
                        "privacy_valid"
                    ]
                )


                st.success(
                    f"Candidate đạt Privacy: "
                    f"{valid_privacy_count}/"
                    f"{len(candidate_strategies)}"
                )


                # 18. MACHINE LEARNING VALIDATION

                ml_rows = []


                for candidate in candidate_strategies:

                    strategy_name = (
                        candidate[
                            "strategy_name"
                        ]
                    )


                    release_data = (
                        candidate_results[
                            strategy_name
                        ][
                            "release_data"
                        ]
                    )


                    retained_indices = (
                        candidate_results[
                            strategy_name
                        ][
                            "retained_indices"
                        ]
                    )


                    # Hàm này thực hiện:
                    #
                    # 1. Align Original và Anonymized
                    # 2. Chia Train / Validation / Test
                    # 3. Train Logistic Regression
                    # 4. Đánh giá Validation
                    # 5. Tính Utility Score
                    ml_validation_result = (
                        ml_evaluator
                        .evaluate_strategy_validation(
                            original_dataframe=data,
                            anonymized_dataframe=release_data,
                            retained_indices=retained_indices,
                            target_column="thu_nhap",
                            random_state=42
                        )
                    )


                    # Lưu toàn bộ kết quả ML.
                    candidate_results[
                        strategy_name
                    ][
                        "ml_validation"
                    ] = ml_validation_result


                    # Utility Score dùng cho Ranking.
                    candidate_results[
                        strategy_name
                    ][
                        "utility_score_percent"
                    ] = (
                        ml_validation_result[
                            "utility_score_percent"
                        ]
                    )


                    original_metrics = (
                        ml_validation_result[
                            "original_metrics"
                        ]
                    )


                    anonymized_metrics = (
                        ml_validation_result[
                            "anonymized_metrics"
                        ]
                    )


                    ml_rows.append(
                        {

                            "Candidate":
                                strategy_name,

                            "Original Accuracy (%)":
                                round(
                                    original_metrics[
                                        "accuracy"
                                    ]
                                    *
                                    100,
                                    2
                                ),

                            "Anonymized Accuracy (%)":
                                round(
                                    anonymized_metrics[
                                        "accuracy"
                                    ]
                                    *
                                    100,
                                    2
                                ),

                            "Original F1 (%)":
                                round(
                                    original_metrics[
                                        "f1_score"
                                    ]
                                    *
                                    100,
                                    2
                                ),

                            "Anonymized F1 (%)":
                                round(
                                    anonymized_metrics[
                                        "f1_score"
                                    ]
                                    *
                                    100,
                                    2
                                ),

                            "Utility Score (%)":
                                round(
                                    ml_validation_result[
                                        "utility_score_percent"
                                    ],
                                    2
                                ),

                            "Validation size":
                                len(
                                    ml_validation_result[
                                        "validation_indices"
                                    ]
                                ),

                            "Reserved Test size":
                                len(
                                    ml_validation_result[
                                        "test_indices"
                                    ]
                                )
                        }
                    )


                # 19. HIỂN THỊ MACHINE LEARNING

                st.header(
                    "7. Đánh giá Utility bằng Machine Learning"
                )


                ml_dataframe = (
                    pd.DataFrame(
                        ml_rows
                    )
                )


                st.dataframe(
                    ml_dataframe,
                    width="stretch",
                    hide_index=True
                )

                # 20. CHUẨN BỊ DỮ LIỆU CHO RANKING

                strategies_for_selection = []


                for candidate in candidate_strategies:

                    strategy_name = (
                        candidate[
                            "strategy_name"
                        ]
                    )


                    current_result = (
                        candidate_results[
                            strategy_name
                        ]
                    )


                    # strategy_selector cần 4 thông tin:
                    #
                    # strategy
                    # suppression_percent
                    # utility_score_percent
                    # privacy_valid
                    strategies_for_selection.append(
                        {

                            "strategy":
                                strategy_name,

                            "suppression_percent":
                                current_result[
                                    "suppression_percent"
                                ],

                            "utility_score_percent":
                                current_result[
                                    "utility_score_percent"
                                ],

                            "privacy_valid":
                                current_result[
                                    "privacy"
                                ][
                                    "privacy_valid"
                                ]
                        }
                    )


                # 21. XẾP HẠNG CANDIDATE

                # Trọng số hiện tại:
                #
                # 50% Data Retention
                # 50% Utility
                ranked_candidates = (
                    strategy_selector
                    .rank_strategies(
                        strategies_for_selection,
                        weight_data_retention=0.5,
                        weight_utility=0.5
                    )
                )


                # 22. CHỌN CANDIDATE TỐT NHẤT

                selected_candidate = (
                    strategy_selector
                    .select_best_strategy(
                        strategies_for_selection,
                        weight_data_retention=0.5,
                        weight_utility=0.5
                    )
                )


                # 23. TẠO BẢNG RANKING

                ranking_rows = []


                for result in ranked_candidates:

                    strategy_name = (
                        result[
                            "strategy"
                        ]
                    )


                    config = (
                        candidate_results[
                            strategy_name
                        ][
                            "config"
                        ]
                    )


                    ranking_rows.append(
                        {

                            "Rank":
                                result[
                                    "rank"
                                ],

                            "Candidate":
                                strategy_name,

                            "Age Level":
                                config[
                                    "age_level"
                                ],

                            "Hours Level":
                                config[
                                    "hours_level"
                                ],

                            "Privacy valid":
                                result[
                                    "privacy_valid"
                                ],

                            "Suppression (%)":
                                round(
                                    result[
                                        "suppression_%"
                                    ],
                                    2
                                ),

                            "Data Retention (%)":
                                round(
                                    result[
                                        "data_retention_%"
                                    ],
                                    2
                                ),

                            "Utility Score (%)":
                                round(
                                    result[
                                        "utility_score_%"
                                    ],
                                    2
                                ),

                            "Selection Score":
                                round(
                                    result[
                                        "selection_score"
                                    ],
                                    2
                                ),

                            "Eligible":
                                result[
                                    "eligible"
                                ]
                        }
                    )


                ranking_dataframe = (
                    pd.DataFrame(
                        ranking_rows
                    )
                    .sort_values(
                        by="Rank"
                    )
                    .reset_index(
                        drop=True
                    )
                )

                # 24. HIỂN THỊ RANKING

                st.header(
                    "8. Xếp hạng và lựa chọn Candidate"
                )


                st.caption(
                    "Selection Score = "
                    "50% Data Retention + 50% Utility Score. "
                    "Candidate phải đạt Privacy mới đủ điều kiện."
                )


                st.dataframe(
                    ranking_dataframe,
                    width="stretch",
                    hide_index=True
                )


                # 25. XỬ LÝ CANDIDATE ĐƯỢC CHỌN

                if selected_candidate is None:

                    st.error(
                        "Không có Candidate nào đủ điều kiện lựa chọn."
                    )


                else:

                    # Tên Candidate thắng.
                    selected_strategy_name = (
                        selected_candidate[
                            "strategy"
                        ]
                    )


                    # Lấy toàn bộ kết quả Candidate thắng.
                    selected_result = (
                        candidate_results[
                            selected_strategy_name
                        ]
                    )


                    st.subheader(
                        "🏆 Candidate được hệ thống lựa chọn"
                    )


                    st.metric(
                        label="Candidate",
                        value=selected_strategy_name
                    )


                    st.success(
                        f"Hệ thống lựa chọn "
                        f"{selected_strategy_name} "
                        f"với Selection Score "
                        f"{selected_candidate['selection_score']:.2f}."
                    )


                    # 26. FINAL TEST

                    st.header(
                        "9. Final Test của Candidate được chọn"
                    )


                    st.info(
                        "Candidate đã được lựa chọn bằng tập Validation. "
                        "Bây giờ hệ thống mới sử dụng tập Test "
                        "được dành riêng để đánh giá cuối cùng."
                    )


                    # Dataset ẩn danh của Candidate thắng.
                    selected_release_data = (
                        selected_result[
                            "release_data"
                        ]
                    )


                    # Index gốc của các bản ghi Candidate thắng.
                    selected_retained_indices = (
                        selected_result[
                            "retained_indices"
                        ]
                    )


                    # Kết quả Validation đã train trước đó.
                    selected_ml_result = (
                        selected_result[
                            "ml_validation"
                        ]
                    )


                    # Chạy Final Test


                    final_test_result = (
                        ml_evaluator
                        .evaluate_selected_strategy_test(

                            original_dataframe=data,

                            anonymized_dataframe=(
                                selected_release_data
                            ),

                            retained_indices=(
                                selected_retained_indices
                            ),

                            validation_result=(
                                selected_ml_result
                            ),

                            target_column="thu_nhap"
                        )
                    )


                    # Lưu Final Test vào kết quả Candidate thắng.
                    candidate_results[
                        selected_strategy_name
                    ][
                        "final_test"
                    ] = final_test_result


                    # 27. LẤY METRIC FINAL TEST

                    original_test_metrics = (
                        final_test_result[
                            "original_metrics"
                        ]
                    )


                    anonymized_test_metrics = (
                        final_test_result[
                            "anonymized_metrics"
                        ]
                    )


                    # 28. HIỂN THỊ THÔNG TIN TẬP TEST

                    test_column_1, \
                    test_column_2, \
                    test_column_3, \
                    test_column_4 = (
                        st.columns(
                            4
                        )
                    )


                    with test_column_1:

                        st.metric(
                            label="Candidate Final Test",
                            value=selected_strategy_name
                        )


                    with test_column_2:

                        st.metric(
                            label="Test size",
                            value=final_test_result[
                                "test_size"
                            ]
                        )


                    with test_column_3:

                        st.metric(
                            label="Cùng Test indices?",
                            value=(
                                "Đúng"
                                if final_test_result[
                                    "same_test_indices"
                                ]
                                else "Sai"
                            )
                        )


                    with test_column_4:

                        st.metric(
                            label="Cùng Test target?",
                            value=(
                                "Đúng"
                                if final_test_result[
                                    "same_test_target"
                                ]
                                else "Sai"
                            )
                        )


                    # =================================================
                    # 29. TẠO BẢNG ORIGINAL VS ANONYMIZED
                    # =================================================

                    # Mỗi dòng là một metric.
                    final_metric_rows = [

                        {
                            "Metric":
                                "Accuracy",

                            "Original (%)":
                                round(
                                    original_test_metrics[
                                        "accuracy"
                                    ]
                                    *
                                    100,
                                    2
                                ),

                            "Anonymized (%)":
                                round(
                                    anonymized_test_metrics[
                                        "accuracy"
                                    ]
                                    *
                                    100,
                                    2
                                )
                        },

                        {
                            "Metric":
                                "Precision",

                            "Original (%)":
                                round(
                                    original_test_metrics[
                                        "precision"
                                    ]
                                    *
                                    100,
                                    2
                                ),

                            "Anonymized (%)":
                                round(
                                    anonymized_test_metrics[
                                        "precision"
                                    ]
                                    *
                                    100,
                                    2
                                )
                        },

                        {
                            "Metric":
                                "Recall",

                            "Original (%)":
                                round(
                                    original_test_metrics[
                                        "recall"
                                    ]
                                    *
                                    100,
                                    2
                                ),

                            "Anonymized (%)":
                                round(
                                    anonymized_test_metrics[
                                        "recall"
                                    ]
                                    *
                                    100,
                                    2
                                )
                        },

                        {
                            "Metric":
                                "F1 Score",

                            "Original (%)":
                                round(
                                    original_test_metrics[
                                        "f1_score"
                                    ]
                                    *
                                    100,
                                    2
                                ),

                            "Anonymized (%)":
                                round(
                                    anonymized_test_metrics[
                                        "f1_score"
                                    ]
                                    *
                                    100,
                                    2
                                )
                        },

                        {
                            "Metric":
                                "Balanced Accuracy",

                            "Original (%)":
                                round(
                                    original_test_metrics[
                                        "balanced_accuracy"
                                    ]
                                    *
                                    100,
                                    2
                                ),

                            "Anonymized (%)":
                                round(
                                    anonymized_test_metrics[
                                        "balanced_accuracy"
                                    ]
                                    *
                                    100,
                                    2
                                )
                        },

                        {
                            "Metric":
                                "ROC-AUC",

                            "Original (%)":
                                round(
                                    original_test_metrics[
                                        "roc_auc"
                                    ]
                                    *
                                    100,
                                    2
                                ),

                            "Anonymized (%)":
                                round(
                                    anonymized_test_metrics[
                                        "roc_auc"
                                    ]
                                    *
                                    100,
                                    2
                                )
                        }
                    ]


                    final_metric_dataframe = (
                        pd.DataFrame(
                            final_metric_rows
                        )
                    )


                    st.subheader(
                        "So sánh Machine Learning trên tập Test"
                    )


                    st.dataframe(
                        final_metric_dataframe,
                        width="stretch",
                        hide_index=True
                    )

                    # 30. FINAL UTILITY SCORE

                    # Utility này được tính trên reserved Test.
                    final_utility = (
                        final_test_result[
                            "utility_score_percent"
                        ]
                    )


                    utility_column_1, utility_column_2 = (
                        st.columns(
                            2
                        )
                    )


                    # Utility dùng ở bước Ranking.
                    with utility_column_1:

                        st.metric(
                            label="Validation Utility",
                            value=(
                                f"{selected_candidate['utility_score_%']:.2f}%"
                            )
                        )


                    # Utility cuối cùng trên Test.
                    with utility_column_2:

                        st.metric(
                            label="Final Test Utility",
                            value=(
                                f"{final_utility:.2f}%"
                            )
                        )


                    # 31. KIỂM TRA TÍNH CÔNG BẰNG CỦA FINAL TEST

                    if (
                        final_test_result[
                            "same_test_indices"
                        ]
                        and
                        final_test_result[
                            "same_test_target"
                        ]
                    ):

                        st.success(
                            "Final Test hoàn thành. "
                            "Original và Anonymized được đánh giá "
                            "trên cùng tập Test và cùng target."
                        )


                    else:

                        st.warning(
                            "Cần kiểm tra lại tập Test vì "
                            "Original và Anonymized chưa khớp."
                        )


                    st.success(
                        f"Final Test Utility Score của "
                        f"{selected_strategy_name}: "
                        f"{final_utility:.2f}%."
                    )


                    st.info(
                        "Final Test chỉ chạy sau khi Candidate "
                        "đã được chọn bằng Validation. "
                        "Tập Test không tham gia vào quá trình Ranking."
                    )


                    # 32. LƯU KẾT QUẢ VÀO SESSION STATE

                    # Streamlit rerun script khi người dùng tương tác.
                    #
                    # Vì vậy lưu dữ liệu vào session_state
                    # giúp các bước biểu đồ và download sau này dùng tiếp.
                    st.session_state[
                        "candidate_results"
                    ] = candidate_results


                    st.session_state[
                        "ranking_dataframe"
                    ] = ranking_dataframe


                    st.session_state[
                        "selected_candidate"
                    ] = selected_candidate


                    st.session_state[
                        "selected_strategy_name"
                    ] = selected_strategy_name


                    st.session_state[
                        "selected_release_data"
                    ] = selected_release_data


                    st.session_state[
                        "final_test_result"
                    ] = final_test_result


                    # Lưu thông tin của lần chạy hiện tại.
                    #
                    # Dùng để tránh hiển thị nhầm kết quả cũ
                    # nếu người dùng đổi file hoặc đổi k/l.
                    st.session_state[
                        "run_file_name"
                    ] = uploaded_file.name


                    st.session_state[
                        "run_k_required"
                    ] = int(
                        k_required
                    )


                    st.session_state[
                        "run_l_required"
                    ] = int(
                        l_required
                    )


                    st.session_state[
                        "run_row_count"
                    ] = len(
                        data
                    )


                    st.success(
                        "Final Test đã hoàn thành."
                    )

        # 33. KIỂM TRA KẾT QUẢ ĐÃ LƯU TRONG SESSION STATE


        required_result_keys = [
            "candidate_results",
            "ranking_dataframe",
            "selected_candidate",
            "selected_strategy_name",
            "selected_release_data",
            "final_test_result"
        ]


        # Chỉ coi là đã có kết quả khi đủ toàn bộ key cần thiết.
        results_available = all(
            key in st.session_state
            for key in required_result_keys
        )

        # - file hiện tại
        # - k hiện tại
        # - l hiện tại
        # - số dòng hiện tại
        # Nhờ vậy không hiển thị nhầm output cũ sau khi rerun.
        current_run_matches = (
            results_available
            and
            st.session_state.get(
                "run_file_name"
            )
            ==
            uploaded_file.name
            and
            st.session_state.get(
                "run_k_required"
            )
            ==
            int(
                k_required
            )
            and
            st.session_state.get(
                "run_l_required"
            )
            ==
            int(
                l_required
            )
            and
            st.session_state.get(
                "run_row_count"
            )
            ==
            len(
                data
            )
        )


        # Nếu có kết quả cũ nhưng cấu hình hiện tại đã thay đổi,
        # yêu cầu chạy lại để tránh hiểu sai kết quả.
        if (
            results_available
            and
            current_run_matches is False
        ):

            st.warning(
                "File hoặc cấu hình k/l hiện tại đã khác lần chạy "
                "gần nhất. Hãy bấm 'Bắt đầu ẩn danh hóa' để tạo "
                "kết quả mới trước khi xem biểu đồ hoặc tải dữ liệu."
            )


        # Chỉ hiển thị output cuối khi kết quả đúng với lần chạy hiện tại.
        if current_run_matches:

            # Lấy các kết quả đã lưu để dùng lại.
            candidate_results_state = (
                st.session_state[
                    "candidate_results"
                ]
            )


            ranking_dataframe_state = (
                st.session_state[
                    "ranking_dataframe"
                ]
                .copy()
            )


            selected_candidate_state = (
                st.session_state[
                    "selected_candidate"
                ]
            )


            selected_strategy_name_state = (
                st.session_state[
                    "selected_strategy_name"
                ]
            )


            selected_release_data_state = (
                st.session_state[
                    "selected_release_data"
                ]
            )


            final_test_result_state = (
                st.session_state[
                    "final_test_result"
                ]
            )

            # 34. BIỂU ĐỒ DATA RETENTION - VALIDATION UTILITY

            st.header(
                "10. Trực quan hóa cân bằng Privacy - Utility"
            )


            st.caption(
                "Trục X là Data Retention sau ẩn danh hóa. "
                "Trục Y là Utility Score trên tập Validation. "
                "Privacy vẫn là điều kiện bắt buộc trước khi Ranking."
            )


            # Tạo Figure và Axis cho biểu đồ Scatter Plot.
            figure, axis = plt.subplots(
                figsize=(
                    10,
                    6
                )
            )


            # Mỗi Candidate được biểu diễn bằng một điểm.
            for _, row in (
                ranking_dataframe_state
                .iterrows()
            ):

                candidate_name = (
                    row[
                        "Candidate"
                    ]
                )


                # Candidate thắng được đánh dấu bằng ngôi sao.
                is_selected = (
                    candidate_name
                    ==
                    selected_strategy_name_state
                )


                # privacy_valid=True chỉ phản ánh việc đạt
                # tiêu chí k/l của thực nghiệm hiện tại.
                # Nó không đồng nghĩa tự động đáp ứng toàn bộ GDPR.
                privacy_valid = bool(
                    row[
                        "Privacy valid"
                    ]
                )


                if is_selected:

                    marker_style = "*"
                    marker_size = 300

                elif privacy_valid is False:

                    marker_style = "x"
                    marker_size = 150

                else:

                    marker_style = "o"
                    marker_size = 120


                # Trục X = Data Retention.
                # Trục Y = Validation Utility.
                axis.scatter(
                    row[
                        "Data Retention (%)"
                    ],
                    row[
                        "Utility Score (%)"
                    ],
                    marker=marker_style,
                    s=marker_size
                )


                # Ghi Rank và tên Candidate cạnh từng điểm.
                axis.annotate(
                    (
                        f"{int(row['Rank'])}. "
                        f"{candidate_name}"
                    ),
                    (
                        row[
                            "Data Retention (%)"
                        ],
                        row[
                            "Utility Score (%)"
                        ]
                    ),
                    xytext=(
                        8,
                        8
                    ),
                    textcoords="offset points",
                    fontsize=9
                )


            axis.set_xlabel(
                "Data Retention (%)"
            )


            axis.set_ylabel(
                "Validation Utility Score (%)"
            )


            axis.set_title(
                "Cân bằng giữa Data Retention "
                "và Machine Learning Utility"
            )


            # Grid giúp dễ đọc vị trí của từng Candidate.
            axis.grid(
                True,
                alpha=0.3
            )


            # Tạo khoảng trống quanh các điểm,
            # tránh nhãn bị sát mép biểu đồ.
            axis.margins(
                x=0.08,
                y=0.12
            )


            # Giúp tiêu đề và nhãn trục không bị cắt.
            figure.tight_layout()


            # Hiển thị biểu đồ trong Streamlit.
            st.pyplot(
                figure,
                clear_figure=True
            )


            st.info(
                "Cách đọc: Candidate càng gần vùng trên bên phải "
                "thì càng giữ lại nhiều dữ liệu và duy trì Utility "
                "tốt hơn. Dấu ★ là Candidate được chọn; dấu × là "
                "Candidate không đạt điều kiện Privacy."
            )


            st.caption(
                "Candidate được chọn là phương án tốt nhất trong "
                "tập Candidate đã đánh giá theo objective hiện tại, "
                "không phải khẳng định tối ưu tuyệt đối."
            )


            # 35. KẾT QUẢ CUỐI CỦA CANDIDATE ĐƯỢC CHỌN

            st.header(
                "11. Kết quả cuối cùng"
            )


            # Lấy toàn bộ kết quả của Candidate thắng.
            selected_result_state = (
                candidate_results_state[
                    selected_strategy_name_state
                ]
            )


            # Lấy kết quả Privacy cuối.
            selected_privacy_state = (
                selected_result_state[
                    "privacy"
                ]
            )


            # Lấy Utility cuối trên reserved Test.
            final_utility_state = (
                final_test_result_state[
                    "utility_score_percent"
                ]
            )


            # 35.1. CÁC CHỈ SỐ TỔNG QUAN

            summary_column_1, \
            summary_column_2, \
            summary_column_3, \
            summary_column_4 = (
                st.columns(
                    4
                )
            )


            with summary_column_1:

                st.metric(
                    label="Candidate được chọn",
                    value=(
                        selected_strategy_name_state
                    )
                )


            with summary_column_2:

                st.metric(
                    label="Privacy",
                    value=(
                        "Đạt"
                        if selected_privacy_state[
                            "privacy_valid"
                        ]
                        else "Không đạt"
                    )
                )


            with summary_column_3:

                st.metric(
                    label="Data Retention",
                    value=(
                        f"{selected_candidate_state['data_retention_%']:.2f}%"
                    )
                )


            with summary_column_4:

                st.metric(
                    label="Suppression",
                    value=(
                        f"{selected_candidate_state['suppression_%']:.2f}%"
                    )
                )


            summary_column_5, \
            summary_column_6, \
            summary_column_7 = (
                st.columns(
                    3
                )
            )


            with summary_column_5:

                st.metric(
                    label="Validation Utility",
                    value=(
                        f"{selected_candidate_state['utility_score_%']:.2f}%"
                    )
                )


            with summary_column_6:

                st.metric(
                    label="Final Test Utility",
                    value=(
                        f"{final_utility_state:.2f}%"
                    )
                )


            with summary_column_7:

                st.metric(
                    label="Selection Score",
                    value=(
                        f"{selected_candidate_state['selection_score']:.2f}"
                    )
                )

            # 35.2. HIỂN THỊ k, l VÀ SỐ DÒNG CUỐI

            privacy_column_1, \
            privacy_column_2, \
            privacy_column_3 = (
                st.columns(
                    3
                )
            )


            with privacy_column_1:

                st.metric(
                    label="k_min cuối",
                    value=(
                        selected_privacy_state[
                            "k_min"
                        ]
                    )
                )


            with privacy_column_2:

                st.metric(
                    label="l_min cuối",
                    value=(
                        selected_privacy_state[
                            "l_min"
                        ]
                    )
                )


            with privacy_column_3:

                st.metric(
                    label="Số bản ghi sau ẩn danh",
                    value=len(
                        selected_release_data_state
                    )
                )


            st.info(
                "Privacy valid=True chỉ cho biết Candidate cuối "
                f"đạt tiêu chí thực nghiệm k={int(k_required)} và "
                f"l={int(l_required)} của hệ thống. Kết quả này "
                "không tự động chứng minh tuân thủ toàn bộ GDPR."
            )
            # 35.3. XEM TRƯỚC DATASET ẨN DANH CUỐI

            st.subheader(
                "Xem trước dataset ẩn danh cuối cùng"
            )


            st.dataframe(
                selected_release_data_state.head(
                    20
                ),
                width="stretch",
                hide_index=True
            )

            # 36. TẢI KẾT QUẢ
            st.header(
                "12. Tải kết quả"
            )


            st.caption(
                "Các file dưới đây được tạo từ Candidate đã được "
                "chọn bằng Validation và đã hoàn thành Final Test."
            )


            # Dataset ẩn danh được xuất CSV.
            anonymized_csv_bytes = (
                selected_release_data_state
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8-sig"
                )
            )


            # retained_indices cho biết những dòng gốc nào
            # còn được giữ lại sau Suppression.
            retained_indices_state = (
                selected_result_state[
                    "retained_indices"
                ]
            )


            retained_indices_dataframe = (
                pd.DataFrame(
                    {
                        "retained_index":
                            list(
                                retained_indices_state
                            )
                    }
                )
            )


            retained_indices_csv_bytes = (
                retained_indices_dataframe
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8-sig"
                )
            )


            # Bảng Ranking cũng được cho phép tải xuống
            # để phục vụ báo cáo và đối chiếu kết quả.
            ranking_csv_bytes = (
                ranking_dataframe_state
                .to_csv(
                    index=False
                )
                .encode(
                    "utf-8-sig"
                )
            )


            download_column_1, \
            download_column_2, \
            download_column_3 = (
                st.columns(
                    3
                )
            )


            with download_column_1:

                st.download_button(
                    label=(
                        "⬇️ Tải dataset ẩn danh"
                    ),
                    data=(
                        anonymized_csv_bytes
                    ),
                    file_name=(
                        f"anonymized_"
                        f"{selected_strategy_name_state}.csv"
                    ),
                    mime="text/csv",
                    width="stretch"
                )


            with download_column_2:

                st.download_button(
                    label=(
                        "⬇️ Tải retained indices"
                    ),
                    data=(
                        retained_indices_csv_bytes
                    ),
                    file_name=(
                        f"retained_indices_"
                        f"{selected_strategy_name_state}.csv"
                    ),
                    mime="text/csv",
                    width="stretch"
                )


            with download_column_3:

                st.download_button(
                    label=(
                        "⬇️ Tải bảng Ranking"
                    ),
                    data=(
                        ranking_csv_bytes
                    ),
                    file_name=(
                        "candidate_ranking.csv"
                    ),
                    mime="text/csv",
                    width="stretch"
                )

            st.success(
                "Pipeline giao diện đã hoàn tất: "
                "Anonymization → Privacy → Validation Utility → "
                "Ranking → Strategy Selection → Final Test → "
                "Visualization → Export."
            )

            st.markdown(
                "<p style='text-align:center; font-size:18px;'>"
                "Cảm ơn mọi người đã sử dụng chương trình."
                "</p>",
                unsafe_allow_html=True
            )

    # 37. BẮT LỖI TOÀN BỘ QUÁ TRÌNH

    except Exception as error:

        # Không để app chết trắng màn hình.
        st.error(
            "Có lỗi xảy ra khi đọc hoặc xử lý dataset."
        )


        # Trong giai đoạn phát triển,
        # hiển thị chi tiết exception để dễ xác định lỗi.
        st.exception(
            error
        )