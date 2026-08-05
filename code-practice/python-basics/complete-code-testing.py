name = input("你叫什么名字？")
print("你好，" + name + "！欢迎来到图书馆！")
books={}
def generate_book_id():
    count=len(books)
    return"B"+str(count+1).zfill(3)
def add_book():
    print("\n---添加新书---")
    title-input("请输入书名").strip()
    auther=input("请输入作者").strip()
    if not title or not author:
        print("书名和作者不能为空！")
        return
    book_id=generate_book_id()
    book_info={
        "title":title,
        "author":author,
        "borrowed":False
    }
    books[book_id]=book_info
    print(f"添加成功！书号：{book_id},书名:<{title}>")
def delete_book():
    print("\n---删除图书---")
    book_id=input("请输入要删除的图书号（如B001）:").strip().upper()
    if book_id in books:
        title=books[book_id]["title"]
        confirm=input(f"请确认删除<{title}>吗？（y/n):").strip().lower()
        if confirm =="y":
            del books[book_id]
            print(f"已删除<{title}>")
        else:
            print("已取消删除")
    else:
        print("未找到该书号")
def update_book():
    print("\n---修改图书信息---")
    book_id=input("请输入要修改的书号：").strip().upper()
if book_id not in books:
    print("没有找到该书号")
return
book=books[book_id]
print(f"当前信息：书名：<{book["title"]}作者:{book['author']}")
new_title = input("请输入新书名（直接回车保留原值）：").strip()
new_author = input("请输入新作者（直接回车保留原值）：").strip()
    if new_title:
    book["title"] = new_title
    if new_author:
        book["author"] = new_author 
        print("✅ 图书信息已更新！")
# ==================== 第7部分：查看所有图书 ====================

def list_books():
    """显示所有图书列表"""
    # 打印一个小标题，告诉用户下面是全部图书
    print("\n--- 全部图书列表 ---")
    
    # 如果柜子是空的（一本书都没有）
    if not books:
        # 打印一个空柜子的图标，告诉用户没书
        print("📭 当前没有图书")
        # 提前结束这个函数，后面的代码不跑了
        return
    
    # 打印表格的列名（书号、书名、作者、状态）
    # :<8 意思是"左对齐，占8个字符的位置"，让表格对齐好看
    print(f"{'书号':<8} {'书名':<15} {'作者':<10} {'状态':<8}")
    # 打印一条分割线，45个减号，把表头和内容分开
    print("-" * 45)
    
    # 循环遍历柜子里的每一本书
    # book_id 是书的标签（比如 B001），info 是这本书的全部信息
    for book_id, info in books.items():
        # 判断这本书的状态
        # 如果 info["borrowed"] 是 True（已借出），status 就存 "已借出"
        # 否则（没借出），status 就存 "可借阅"
        status = "已借出" if info["borrowed"] else "可借阅"
        # 打印这一行：书号、书名、作者、状态，对齐排列
        print(f"{book_id:<8} {info['title']:<15} {info['author']:<10} {status:<8}")


# ==================== 第8部分：搜索图书 ====================

def search_book():
    """根据书名或作者搜索图书"""
    # 打印小标题
    print("\n--- 搜索图书 ---")
    # 让用户输入关键词，去掉首尾空格
    keyword = input("请输入搜索关键词（书名或作者）：").strip()
    
    # 如果用户啥都没输入（直接按回车了）
    if not keyword:
        # 提示关键词不能为空
        print("❌ 关键词不能为空！")
        # 提前结束函数
        return
    
    # 创建一个空列表，用来存放找到的书
    # [] 是空列表，后面用 .append() 往里面加东西
    results = []
    
    # 循环遍历柜子里的每一本书
    for book_id, info in books.items():
        # 检查关键词是否出现在书名里（不区分大小写）
        # .lower() 把文字全部转成小写，这样搜索 "python" 和 "Python" 都能找到
        # 或者关键词出现在作者里
        if keyword.lower() in info["title"].lower() or keyword.lower() in info["author"].lower():
            # 如果找到了，把这本书（书号和全部信息）加到结果列表里
            # .append() 是"追加"的意思，往列表最后面添加
            results.append((book_id, info))
    
    # 如果找到了至少一本书
    if results:
        # 打印找到几本
        print(f"找到 {len(results)} 本相关图书：")
        # 打印表头
        print(f"{'书号':<8} {'书名':<15} {'作者':<10} {'状态':<8}")
        print("-" * 45)
        # 循环遍历结果列表里的每一本
        for book_id, info in results:
            # 判断状态
            status = "已借出" if info["borrowed"] else "可借阅"
            # 打印这一本书的信息
            print(f"{book_id:<8} {info['title']:<15} {info['author']:<10} {status:<8}")
    else:
        # 一本书都没找到
        print("❌ 未找到匹配的图书")


# ==================== 第9部分：借阅图书 ====================

def borrow_book():
    """借阅图书（把状态改成已借出）"""
    # 打印小标题
    print("\n--- 借阅图书 ---")
    # 让用户输入要借的书号，去掉空格，转成大写
    book_id = input("请输入要借阅的书号：").strip().upper()
    
    # 检查这本书在不在柜子里
    if book_id not in books:
        # 不在就提示
        print("❌ 未找到该书号！")
        # 提前结束
        return
    
    # 从柜子里拿出这本书的全部信息
    book = books[book_id]
    
    # 检查这本书是否已经借出去了
    # 如果 borrowed 是 True（已借出）
    if book["borrowed"]:
        # 提示已被借出
        print(f"❌ 《{book['title']}》已被借出，无法再次借阅")
    else:
        # 否则（没借出去），把状态改成 True（已借出）
        book["borrowed"] = True
        # 提示借阅成功
        print(f"✅ 成功借阅《{book['title']}》")


# ==================== 第10部分：归还图书 ====================

def return_book():
    """归还图书（把状态改成可借阅）"""
    # 打印小标题
    print("\n--- 归还图书 ---")
    # 让用户输入要还的书号，去掉空格，转成大写
    book_id = input("请输入要归还的书号：").strip().upper()
    
    # 检查这本书在不在柜子里
    if book_id not in books:
        # 不在就提示
        print("❌ 未找到该书号！")
        # 提前结束
        return
    
    # 从柜子里拿出这本书的全部信息
    book = books[book_id]
    
    # 检查这本书是不是借出状态
    # 如果 not book["borrowed"] 意思是"没借出去"（borrowed 是 False）
    if not book["borrowed"]:
        # 没借出去就提示无需归还
        print(f"❌ 《{book['title']}》未被借出，无需归还")
    else:
        # 否则（借出去了），把状态改成 False（可借阅）
        book["borrowed"] = False
        # 提示归还成功
        print(f"✅ 成功归还《{book['title']}》")


# ==================== 第11部分：显示菜单 ====================

def show_menu():
    """显示主菜单（就是打印那堆数字选项）"""
    # 先空一行，然后打印一排等号（35个）
    print("\n" + "=" * 35)
    # 打印标题，居中显示
    print("      📚 图书管理系统")
    # 再打印一排等号
    print("=" * 35)
    # 打印所有菜单选项
    print("1. 添加图书")
    print("2. 删除图书")
    print("3. 修改图书信息")
    print("4. 查看全部图书")
    print("5. 搜索图书")
    print("6. 借阅图书")
    print("7. 归还图书")
    print("0. 退出系统")
    # 打印一排减号收尾
    print("-" * 35)


# ==================== 第12部分：主程序（总指挥） ====================

def main():
    """程序的总指挥，负责一直循环显示菜单并执行操作"""
    # 打印欢迎语
    print("欢迎使用图书管理系统！")
    
    # 往柜子里放3本示例书，方便你直接测试，不用自己加
    # books["B001"] 意思是：在柜子里用 "B001" 当标签
    # 后面花括号里是这本书的信息：书名、作者、是否借出
    books["B001"] = {"title": "Python入门", "author": "张三", "borrowed": False}
    books["B002"] = {"title": "数据结构", "author": "李四", "borrowed": True}
    books["B003"] = {"title": "算法导论", "author": "王五", "borrowed": False}
    # 提示用户已经加载了示例数据
    print("已加载示例数据，输入对应数字进行操作。")
    
    # 无限循环（while True 意思是"一直重复"）
    # 只有遇到 break 才会跳出循环
    while True:
        # 调用上面的 show_menu() 函数，打印菜单
        show_menu()
        # 让用户输入一个数字，去掉空格
        choice = input("请输入操作编号：").strip()
        
        # 判断用户输入的是几，就执行对应的功能
        # == 是"等于"的意思，比较两边是否相等
        if choice == '1':
            add_book()          # 调用添加图书的函数
        elif choice == '2':
            delete_book()       # 调用删除图书的函数
        elif choice == '3':
            update_book()       # 调用修改图书的函数
        elif choice == '4':
            list_books()        # 调用查看全部图书的函数
        elif choice == '5':
            search_book()       # 调用搜索图书的函数
        elif choice == '6':
            borrow_book()       # 调用借阅图书的函数
        elif choice == '7':
            return_book()       # 调用归还图书的函数
        elif choice == '0':
            # 用户要退出
            print("感谢使用，再见！")
            break               # break 是"跳出循环"，程序结束
        else:
            # 用户输入了 0-7 以外的数字
            print("❌ 无效输入，请重新选择")
        
        # 每次操作完，暂停一下
        # input() 在这里的作用是"等用户按回车"，让你看到结果再继续
        input("\n按 Enter 键继续...")


# ==================== 第13部分：程序入口 ====================

# 这句话的意思是：只有直接运行这个文件时，才执行 main()
# 如果这个文件被别的文件导入（比如 import），就不会自动运行
# __name__ 是 Python 的一个特殊变量
# 直接运行这个文件时，__name__ 的值是 "__main__"
# 被别的文件导入时，__name__ 的值是文件名
if __name__ == "__main__":
    # 调用主函数，程序开始运行
    main()