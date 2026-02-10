import json
import os


DATA_FILE = "products.json"

def load_data():
    """
    Đọc dữ liệu từ file products.json.
    Nếu file không tồn tại, trả về danh sách rỗng.
    """
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
       
        return []
    except json.JSONDecodeError:
        
        return []

def save_data(products):
    """
    Ghi danh sách sản phẩm vào file products.json.
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
        
            json.dump(products, f, indent=4, ensure_ascii=False)
        print(">> Đã lưu dữ liệu thành công!")
    except Exception as e:
        print(f"Lỗi khi lưu file: {e}")

def add_product(products):
    """
    Thêm sản phẩm mới vào danh sách.
    Tự động sinh mã ID (Ví dụ: LT01, LT02...).
    """
    print("\n--- THÊM SẢN PHẨM MỚI ---")
    name = input("Nhập tên sản phẩm: ")
    brand = input("Nhập thương hiệu: ")
    
   
    while True:
        try:
            price = int(input("Nhập giá sản phẩm : "))
            quantity = int(input("Nhập số lượng tồn kho : "))
            if price < 0 or quantity < 0:
                print("Giá và số lượng phải lớn hơn hoặc bằng 0.")
                continue
            break
        except Exception:
            print("Vui lòng nhập con số hợp lệ!")

   
    new_id = f"LT{len(products) + 1:02d}" 
    
 
    existing_ids = [p['id'] for p in products]
    count = len(products) + 1
    while new_id in existing_ids:
        count += 1
        new_id = f"LT{count:02d}"

    new_product = {
        "id": new_id,
        "name": name,
        "brand": brand,
        "price": price,
        "quantity": quantity
    }
    
    products.append(new_product)
    print(f"Đã thêm sản phẩm thành công! Mã sản phẩm: {new_id}")
    return products

def update_product(products):
    """
    Cập nhật thông tin sản phẩm dựa trên ID.
    """
    print("\n--- CẬP NHẬT SẢN PHẨM ---")
    product_id = input("Nhập mã sản phẩm cần sửa (VD: LT01): ").strip()
    
    found = False
    for product in products:
        if product['id'] == product_id:
            found = True
            print(f"Tìm thấy: {product['name']}")
            print("Nhập thông tin mới (nếu không đổi, hãy nhập lại giá trị cũ):")
            
            product['name'] = input(f"Tên mới ({product['name']}): ") or product['name']
            product['brand'] = input(f"Thương hiệu mới ({product['brand']}): ") or product['brand']
            
       
            try:
                p_input = input(f"Giá mới ({product['price']}): ")
                if p_input:
                    product['price'] = int(p_input)
                
                q_input = input(f"Số lượng mới ({product['quantity']}): ")
                if q_input:
                    product['quantity'] = int(q_input)
            except ValueError:
                print("Lỗi nhập liệu số! Giữ nguyên giá trị cũ.")

            print("Cập nhật thành công!")
            break
    
    if not found:
        print(f"Không tìm thấy sản phẩm có mã {product_id}")
    
    return products

def delete_product(products):
    """
    Xóa sản phẩm khỏi danh sách theo ID (Cải tiến: Không phân biệt hoa thường).
    """
    print("\n--- XÓA SẢN PHẨM ---")
    
    
    input_id = input("Nhập mã sản phẩm cần xóa (VD: LT01): ").strip().upper()
    
    found_product = None
    
    
    for p in products:
       
        if p['id'].upper() == input_id:
            found_product = p
            break
    
    
    if found_product:
        print(f"Đã tìm thấy sản phẩm: {found_product['name']} (Giá: {found_product['price']})")
        confirm = input(f"Bạn chắc chắn muốn xóa không? (y/n): ")
        
        if confirm.lower() == 'y':
            products.remove(found_product)
            print(">> Đã xóa thành công!")
        else:
            print(">> Đã hủy thao tác xóa.")
    else:
        print(f">> KHÔNG TÌM THẤY mã sản phẩm '{input_id}'.")
        
        
        print("Các mã sản phẩm hiện có trong kho:", end=" ")
        ids = [p['id'] for p in products]
        print(", ".join(ids))

    return products
def search_product_by_name(products):
    """
    Tìm kiếm sản phẩm theo từ khóa (gần đúng, không phân biệt hoa thường).
    """
    print("\n--- TÌM KIẾM SẢN PHẨM ---")
    keyword = input("Nhập tên sản phẩm cần tìm: ").lower()
    
    results = [p for p in products if keyword in p['name'].lower()]
    
    if results:
        print(f"\nTìm thấy {len(results)} kết quả:")
        display_all_products(results) 
    else:
        print(f"Không tìm thấy sản phẩm nào chứa từ khóa '{keyword}'")

def display_all_products(products):
    """
    Hiển thị danh sách sản phẩm dạng bảng.
    """
    if not products:
        print("\n>> Kho hàng trống.")
        return

    print("\n" + "="*85)
    print(f"{'MÃ':<10} | {'TÊN SẢN PHẨM':<30} | {'THƯƠNG HIỆU':<15} | {'GIÁ':<12} | {'SL':<5}")
    print("-" * 85)
    
    for p in products:
        
        formatted_price = "{:,}".format(p['price'])
        print(f"{p['id']:<10} | {p['name']:<30} | {p['brand']:<15} | {formatted_price:<12} | {p['quantity']:<5}")
    
    print("="*85 + "\n")