
# Kiểm thử các module chính của hệ thống ẩn danh hóa dữ liệu.
# Ta không chỉ kiểm tra trường hợp dữ liệu đúng,
# mà còn cố tình đưa dữ liệu/cấu hình sai vào hệ thống
# để xem chương trình có phát hiện lỗi hay không.
# Kết quả kiểm thử sẽ được lưu thành file:


from pathlib import Path

import sys


import pandas as pd

# 2. XÁC ĐỊNH PROJECT ROOT
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


# Thêm src vào sys.path nếu chưa tồn tại.
if str(SRC_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(SRC_DIR)
    )

# 4. IMPORT MODULE CỦA ĐỒ ÁN

import anonymization_engine
import strategy_generator


# 5. XÁC ĐỊNH DATASET

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "dataset_anonymization.csv"
)


# Kiểm tra dataset có tồn tại.
if not DATA_FILE.exists():

    raise FileNotFoundError(
        f"Không tìm thấy dataset: {DATA_FILE}"
    )


# Đọc dataset gốc.
data = pd.read_csv(
    DATA_FILE
)

# 6. THƯ MỤC LƯU KẾT QUẢ KIỂM THỬ

OUTPUT_DIR = (
    PROJECT_ROOT
    / "outputs_bieu_do_ket_qua"
)


# Tạo thư mục nếu chưa có.
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# File kết quả kiểm thử.
TEST_RESULT_FILE = (
    OUTPUT_DIR
    / "ket_qua_kiem_thu_he_thong.csv"
)


# 7. DANH SÁCH LƯU KẾT QUẢ TEST
test_results = []

# 8. HÀM LƯU KẾT QUẢ MỘT TEST CASE

def add_test_result(
    test_id,
    test_name,
    expected_result,
    actual_result,
    status
):
    """
    Thêm kết quả của một Test Case
    vào danh sách test_results.
    """

    test_results.append(
        {
            "test_id": test_id,
            "test_name": test_name,
            "expected_result": expected_result,
            "actual_result": actual_result,
            "status": status
        }
    )

# 9. HÀM CHẠY TEST MONG ĐỢI THÀNH CÔNG

def run_success_test(
    test_id,
    test_name,
    test_function
):
    """
    Chạy một Test Case mà kết quả mong đợi
    là chương trình phải chạy thành công.
    """

    try:

        # Chạy hàm kiểm thử.
        actual_result = (
            test_function()
        )


        # Nếu không phát sinh Exception
        # thì xem là PASS.
        add_test_result(
            test_id=test_id,
            test_name=test_name,
            expected_result="Chạy thành công",
            actual_result=str(actual_result),
            status="PASS"
        )


    except Exception as error:

        # Nếu phát sinh lỗi ngoài mong đợi
        # thì Test Case thất bại.
        add_test_result(
            test_id=test_id,
            test_name=test_name,
            expected_result="Chạy thành công",
            actual_result=(
                f"{type(error).__name__}: {error}"
            ),
            status="FAIL"
        )

# 10. HÀM CHẠY TEST MONG ĐỢI PHẢI BÁO LỖI
def run_error_test(
    test_id,
    test_name,
    test_function,
    expected_exception
):
    """
    Chạy Test Case mà hệ thống
    bắt buộc phải phát hiện lỗi.
    """

    try:

        # Chạy tình huống cố tình sai.
        test_function()


        # Nếu chạy tới đây mà KHÔNG phát sinh lỗi,
        # nghĩa là hệ thống chưa kiểm tra đầu vào đầy đủ.
        add_test_result(
            test_id=test_id,
            test_name=test_name,
            expected_result=(
                f"Phải phát sinh {expected_exception.__name__}"
            ),
            actual_result="Không phát sinh lỗi",
            status="FAIL"
        )


    except expected_exception as error:

        # Phát sinh đúng loại lỗi mong đợi.
        add_test_result(
            test_id=test_id,
            test_name=test_name,
            expected_result=(
                f"Phải phát sinh {expected_exception.__name__}"
            ),
            actual_result=(
                f"{type(error).__name__}: {error}"
            ),
            status="PASS"
        )


    except Exception as error:

        # Có báo lỗi nhưng sai loại lỗi mong đợi.
        add_test_result(
            test_id=test_id,
            test_name=test_name,
            expected_result=(
                f"Phải phát sinh {expected_exception.__name__}"
            ),
            actual_result=(
                f"{type(error).__name__}: {error}"
            ),
            status="FAIL"
        )

# 11. TC01 - DATASET HỢP LỆ

def test_valid_dataset():
    """
    Kiểm tra Candidate hợp lệ
    có thể chạy ẩn danh hóa thành công hay không.
    """

    # Lấy Candidate đầu tiên.
    candidate = (
        strategy_generator
        .generate_candidate_strategies()[
            0
        ]
    )


    # Chạy ẩn danh hóa.
    release_data, retained_indices = (
        anonymization_engine
        .anonymize_candidate_strategy(
            dataframe=data,
            strategy_config=candidate,
            k_required=5,
            l_required=2
        )
    )


    # Kiểm tra số dòng và retained indices.
    if (
        len(release_data)
        !=
        len(retained_indices)
    ):

        raise ValueError(
            "release_data và retained_indices không khớp."
        )


    return (
        f"Release shape = {release_data.shape}"
    )


# Chạy TC01.
run_success_test(
    test_id="TC01",
    test_name="Dataset hợp lệ",
    test_function=test_valid_dataset
)

# 12. TC02 - STRATEGY GENERATOR SINH ĐÚNG 4 CANDIDATE
def test_candidate_generator():

    # Sinh Candidate tự động.
    candidates = (
        strategy_generator
        .generate_candidate_strategies()
    )


    # Đồ án hiện tại sử dụng đúng 4 Candidate.
    if len(candidates) != 4:

        raise ValueError(
            "Số Candidate không bằng 4."
        )


    # Kiểm tra cấu hình Candidate.
    strategy_generator.validate_candidate_strategies(
        candidates
    )


    return (
        f"Số Candidate = {len(candidates)}"
    )


# Chạy TC02.
run_success_test(
    test_id="TC02",
    test_name="Sinh tự động 4 Candidate",
    test_function=test_candidate_generator
)

# 13. TC03 - DATASET THIẾU CỘT THU_NHAP
def test_missing_target():

    # Tạo dataset cố tình xóa cột thu_nhap.
    invalid_data = (
        data.drop(
            columns=[
                "thu_nhap"
            ]
        )
    )


    # Lấy Candidate hợp lệ.
    candidate = (
        strategy_generator
        .generate_candidate_strategies()[
            0
        ]
    )


    # Hệ thống phải phát hiện lỗi
    # vì thu_nhap là thuộc tính nhạy cảm.
    anonymization_engine.anonymize_candidate_strategy(
        dataframe=invalid_data,
        strategy_config=candidate,
        k_required=5,
        l_required=2
    )


# Chạy TC03.
run_error_test(
    test_id="TC03",
    test_name="Dataset thiếu cột thu_nhap",
    test_function=test_missing_target,
    expected_exception=KeyError
)

# 14. TC04 - DATASET THIẾU CỘT TUỔI
def test_missing_age_column():

    # Xóa cột tuoi khỏi dataset.
    invalid_data = (
        data.drop(
            columns=[
                "tuoi"
            ]
        )
    )


    candidate = (
        strategy_generator
        .generate_candidate_strategies()[
            0
        ]
    )


    anonymization_engine.anonymize_candidate_strategy(
        dataframe=invalid_data,
        strategy_config=candidate,
        k_required=5,
        l_required=2
    )


# Chạy TC04.
run_error_test(
    test_id="TC04",
    test_name="Dataset thiếu cột QI tuổi",
    test_function=test_missing_age_column,
    expected_exception=KeyError
)

# 15. TC05 - CANDIDATE THIẾU AGE_LEVEL
def test_missing_age_level():

    # Candidate cố tình thiếu age_level.
    invalid_config = {
        "strategy_name": "candidate_test",
        "hours_level": "hours3"
    }


    anonymization_engine.anonymize_candidate_strategy(
        dataframe=data,
        strategy_config=invalid_config,
        k_required=5,
        l_required=2
    )


# Chạy TC05.
run_error_test(
    test_id="TC05",
    test_name="Candidate thiếu age_level",
    test_function=test_missing_age_level,
    expected_exception=ValueError
)

# 16. TC06 - CANDIDATE THIẾU HOURS_LEVEL

def test_missing_hours_level():

    # Candidate cố tình thiếu hours_level.
    invalid_config = {
        "strategy_name": "candidate_test",
        "age_level": "age3"
    }


    anonymization_engine.anonymize_candidate_strategy(
        dataframe=data,
        strategy_config=invalid_config,
        k_required=5,
        l_required=2
    )


# Chạy TC06.
run_error_test(
    test_id="TC06",
    test_name="Candidate thiếu hours_level",
    test_function=test_missing_hours_level,
    expected_exception=ValueError
)

# 17. TC07 - AGE LEVEL KHÔNG HỢP LỆ
def test_invalid_age_level():

    invalid_config = {
        "strategy_name": "candidate_test",
        "age_level": "age_sai",
        "hours_level": "hours3"
    }


    anonymization_engine.anonymize_candidate_strategy(
        dataframe=data,
        strategy_config=invalid_config,
        k_required=5,
        l_required=2
    )


# Chạy TC07.
run_error_test(
    test_id="TC07",
    test_name="age_level không hợp lệ",
    test_function=test_invalid_age_level,
    expected_exception=ValueError
)

# 18. TC08 - HOURS LEVEL KHÔNG HỢP LỆ

def test_invalid_hours_level():

    invalid_config = {
        "strategy_name": "candidate_test",
        "age_level": "age3",
        "hours_level": "hours_sai"
    }


    anonymization_engine.anonymize_candidate_strategy(
        dataframe=data,
        strategy_config=invalid_config,
        k_required=5,
        l_required=2
    )


# Chạy TC08.
run_error_test(
    test_id="TC08",
    test_name="hours_level không hợp lệ",
    test_function=test_invalid_hours_level,
    expected_exception=ValueError
)


# 19. TC09 - K KHÔNG HỢP LỆ
def test_invalid_k():

    candidate = (
        strategy_generator
        .generate_candidate_strategies()[
            0
        ]
    )


    # k=0 là không hợp lệ.
    anonymization_engine.anonymize_candidate_strategy(
        dataframe=data,
        strategy_config=candidate,
        k_required=0,
        l_required=2
    )


# Chạy TC09.
run_error_test(
    test_id="TC09",
    test_name="k_required bằng 0",
    test_function=test_invalid_k,
    expected_exception=ValueError
)

# 20. TC10 - L KHÔNG HỢP LỆ

def test_invalid_l():

    candidate = (
        strategy_generator
        .generate_candidate_strategies()[
            0
        ]
    )


    # l=0 là không hợp lệ.
    anonymization_engine.anonymize_candidate_strategy(
        dataframe=data,
        strategy_config=candidate,
        k_required=5,
        l_required=0
    )


# Chạy TC10.
run_error_test(
    test_id="TC10",
    test_name="l_required bằng 0",
    test_function=test_invalid_l,
    expected_exception=ValueError
)

# 21. TẠO DATAFRAME KẾT QUẢ
test_result_dataframe = pd.DataFrame(
    test_results
)

# 22. LƯU FILE KẾT QUẢ KIỂM THỬ
test_result_dataframe.to_csv(
    TEST_RESULT_FILE,
    index=False
)

# 23. THỐNG KÊ PASS / FAIL
pass_count = (
    test_result_dataframe[
        "status"
    ]
    .eq(
        "PASS"
    )
    .sum()
)


fail_count = (
    test_result_dataframe[
        "status"
    ]
    .eq(
        "FAIL"
    )
    .sum()
)


total_count = (
    len(
        test_result_dataframe
    )
)

# 24. HIỂN THỊ KẾT QUẢ

print(
    "===== KIỂM THỬ HỆ THỐNG ====="
)


print(
    test_result_dataframe.to_string(
        index=False
    )
)


print(
    "\n===== TỔNG KẾT ====="
)


print(
    "Tổng Test Case:",
    total_count
)


print(
    "PASS:",
    pass_count
)


print(
    "FAIL:",
    fail_count
)


print(
    "File kết quả:",
    TEST_RESULT_FILE
)


print(
    "System Tester: Chúc mừng bạn đã chạy hoàn thành"
)