import logging

# Cấu hình Logging
logging.basicConfig(
    filename='fantasy_league.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Dữ liệu ban đầu
players = [
    {
        "player_id": "T101",
        "name": "Faker",
        "market_value": 5000,
        "fan_tokens": 1500,
        "match_points": 0,
        "form_multiplier": 1.0
    },
    {
        "player_id": "GEN01",
        "name": "Chovy",
        "market_value": 4800,
        "fan_tokens": 800,
        "match_points": 500,
        "form_multiplier": 1.2
    },
    {
        "player_id": "DRX01",
        "name": "Deft",
        "market_value": 3000,
        "fan_tokens": 0,
        "match_points": 0,
        "form_multiplier": 0.8
    }
]


def find_player_by_id(players_list: list, player_id: str) -> int:
    """Tìm index của tuyển thủ theo player_id. Trả về -1 nếu không tìm thấy."""
    pid = player_id.strip().upper()
    for i, player in enumerate(players_list):
        if player.get("player_id") == pid:
            return i
    return -1


def get_investment_status(fan_tokens: int) -> str:
    """Xác định trạng thái đầu tư."""
    if fan_tokens == 0:
        return "Chưa có người đầu tư"
    elif fan_tokens <= 1000:
        return "Đang thu hút"
    return "Tuyển thủ Hot"


def display_market(players_list: list) -> None:
    """Hiển thị sàn giao dịch tuyển thủ."""
    logging.info("User viewed the player market.")
    print("\n--- SÀN GIAO DỊCH TUYỂN THỦ ---")
    if not players_list:
        print("Sàn giao dịch hiện chưa có tuyển thủ nào.")
        return

    print(f"{'ID':<8} | {'Tên tuyển thủ':<12} | {'Giá trị TT':<10} | {'Fan Token':<9} | "
          f"{'Điểm trận':<8} | {'Hệ số':<6} | Trạng thái đầu tư")
    print("-" * 100)
    for p in players_list:
        status = get_investment_status(p.get("fan_tokens", 0))
        print(f"{p.get('player_id','N/A'):<8} | {p.get('name','Unknown'):<12} | "
              f"{p.get('market_value',0):>10,} | {p.get('fan_tokens',0):>9,} | "
              f"{p.get('match_points',0):>8} | {p.get('form_multiplier',1.0):>5.1f} | {status}")


def invest_tokens(players_list: list) -> None:
    """Đầu tư Fan Token vào tuyển thủ."""
    print("\n--- ĐẦU TƯ FAN TOKEN ---")
    try:
        player_id = input("Nhập mã tuyển thủ: ").strip()
        idx = find_player_by_id(players_list, player_id)
        if idx == -1:
            print("Không tìm thấy tuyển thủ!")
            logging.warning(f"Invest failed - Player {player_id.upper()} not found")
            return

        player = players_list[idx]
        while True:
            try:
                amount = int(input("Nhập số token muốn đầu tư: ").strip())
                if amount <= 0:
                    print("Số token phải là số nguyên dương. Vui lòng nhập lại.")
                    continue
                break
            except ValueError:
                print("Số token phải là số nguyên dương. Vui lòng nhập lại.")
                logging.warning("Invalid token input while investing")

        player["fan_tokens"] = player.get("fan_tokens", 0) + amount
        print(f"Thành công: Đã đầu tư {amount} token vào tuyển thủ {player.get('player_id')}.")
        print(f"Số Fan Token hiện tại của {player.get('name')}: {player['fan_tokens']:,}")
        logging.info(f"Invested {amount} tokens into {player.get('player_id')}")

    except Exception as e:
        logging.error(f"Error investing tokens: {e}")


def calc_actual_withdrawal(withdraw_amount: float) -> float:
    """Tính số token thực nhận sau khi trừ 10% phí."""
    if withdraw_amount < 0:
        raise ValueError("Số token rút không được âm")
    return withdraw_amount * 0.9


def withdraw_tokens(players_list: list) -> None:
    """Rút vốn Fan Token."""
    print("\n--- RÚT VỐN FAN TOKEN ---")
    try:
        player_id = input("Nhập mã tuyển thủ: ").strip()
        idx = find_player_by_id(players_list, player_id)
        if idx == -1:
            print("Không tìm thấy tuyển thủ!")
            logging.warning(f"Withdraw failed - Player {player_id.upper()} not found")
            return

        player = players_list[idx]
        current_tokens = player.get("fan_tokens", 0)

        while True:
            try:
                amount = int(input("Nhập số token muốn rút: ").strip())
                if amount <= 0:
                    print("Số token phải là số nguyên dương. Vui lòng nhập lại.")
                    continue
                if amount > current_tokens:
                    print(f"Không thể rút. Số token muốn rút vượt quá số Fan Token hiện có.")
                    print(f"Fan Token hiện có của {player.get('name')}: {current_tokens}")
                    logging.warning(f"Withdraw failed - Amount exceeds current fan tokens")
                    return
                break
            except ValueError:
                print("Số token phải là số nguyên dương. Vui lòng nhập lại.")

        actual_received = calc_actual_withdrawal(amount)
        player["fan_tokens"] -= amount

        print(f"Thành công: Đã rút {amount} token khỏi tuyển thủ {player.get('player_id')}.")
        print(f"Phí giao dịch 10%: {amount * 0.1:.1f} token")
        print(f"Số token thực nhận về ví: {actual_received:.1f} token")
        print(f"Fan Token còn lại của {player.get('name')}: {player['fan_tokens']:,}")
        logging.info(f"Withdrawn {amount} tokens from {player.get('player_id')}. Actual received: {actual_received}")

    except Exception as e:
        logging.error(f"Error withdrawing tokens: {e}")


def update_form(players_list: list) -> None:
    """Cập nhật hệ số phong độ."""
    print("\n--- CẬP NHẬT HỆ SỐ PHONG ĐỘ ---")
    try:
        player_id = input("Nhập mã tuyển thủ: ").strip()
        idx = find_player_by_id(players_list, player_id)
        if idx == -1:
            print("Không tìm thấy tuyển thủ!")
            return

        player = players_list[idx]
        while True:
            try:
                multiplier = float(input("Nhập hệ số phong độ mới (0.5 - 2.5): ").strip())
                if not 0.5 <= multiplier <= 2.5:
                    print("Hệ số phong độ chỉ được nằm trong khoảng 0.5 đến 2.5.")
                    continue
                break
            except ValueError:
                print("Hệ số phong độ phải là số thực. Vui lòng nhập lại.")

        player["form_multiplier"] = multiplier
        print(f"Thành công: Đã cập nhật hệ số phong độ cho {player.get('name')}.")
        print(f"Hệ số mới: x{multiplier}")
        logging.info(f"Updated form multiplier for {player.get('player_id')} to {multiplier}")

    except Exception as e:
        logging.error(f"Error updating form: {e}")


def calculate_match_points(players_list: list) -> None:
    """Chấm điểm sau trận đấu."""
    print("\n--- CHẤM ĐIỂM SAU TRẬN ĐẤU ---")
    try:
        player_id = input("Nhập mã tuyển thủ: ").strip()
        idx = find_player_by_id(players_list, player_id)
        if idx == -1:
            print("Không tìm thấy tuyển thủ!")
            return

        player = players_list[idx]
        base_points = float(input("Nhập điểm gốc của trận đấu: ").strip())

        actual_points = base_points * player.get("form_multiplier", 1.0)
        player["match_points"] = player.get("match_points", 0) + actual_points

        print(f">> Tuyển thủ {player.get('name')} nhận được {actual_points:.0f} điểm (Hệ số x{player.get('form_multiplier',1.0):.1f}).")
        print(f"Tổng điểm: {player['match_points']:.0f}")
        logging.info(f"Added {actual_points} match points to {player.get('player_id')}")

    except ValueError:
        print("Điểm số phải là số. Vui lòng nhập lại.")
    except Exception as e:
        logging.error(f"Error calculating match points: {e}")


def show_menu() -> None:
    print("\n===== HỆ THỐNG RIKKEI ESPORTS FANTASY =====")
    print("1. Xem Sàn Giao Dịch Tuyển Thủ")
    print("2. Đầu tư Fan Token")
    print("3. Rút vốn (Hoàn trả Token)")
    print("4. Biến động phong độ (Cập nhật hệ số)")
    print("5. Chấm điểm sau trận đấu")
    print("6. Thoát hệ thống")
    print("=" * 50)


def main() -> None:
    while True:
        show_menu()
        try:
            choice = input("Chọn chức năng (1-6): ").strip()
            if choice == "1":
                display_market(players)
            elif choice == "2":
                invest_tokens(players)
            elif choice == "3":
                withdraw_tokens(players)
            elif choice == "4":
                update_form(players)
            elif choice == "5":
                calculate_match_points(players)
            elif choice == "6":
                logging.info("System shutdown.")
                print("Đóng hệ thống Rikkei Esports Fantasy.")
                break
            else:
                print("Lựa chọn không hợp lệ!")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()