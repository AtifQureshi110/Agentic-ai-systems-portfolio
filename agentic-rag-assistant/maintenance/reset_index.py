from vectorstore.pinecone_client import (
    delete_all_vectors,
    delete_by_source,
    get_index_stats,
    get_all_sources
)


def reset_index():

    print("\n==============================")
    print("PINECONE MAINTENANCE TOOL")
    print("==============================\n")

    print("Choose an option:")
    print("1 Delete FULL index")
    print("2 Delete SPECIFIC document by selecting source")
    print("3 Show index stats")
    print("4 Exit\n")

    choice = input("Enter choice (1-4): ").strip()

    # ---------------- FULL DELETE ----------------
    if choice == "1":

        confirm = input("\n Type YES/yes to delete FULL index: ").strip()

        if confirm == "YES" or confirm == "yes":
            delete_all_vectors()
            print(" Entire index deleted successfully")
        else:
            print(" Cancelled")


    # ---------------- DELETE BY SOURCE (SELECT UI) ----------------
    elif choice == "2":

        sources = get_all_sources()

        if not sources:
            print(" No sources found in index")
            return

        print("\n Available Documents:\n")

        for i, src in enumerate(sources):
            print(f"{i + 1}. {src}")

        print("\n")

        try:
            index_choice = int(input("Select document number to delete: ")) - 1
        except ValueError:
            print(" Invalid input")
            return

        if index_choice < 0 or index_choice >= len(sources):
            print(" Invalid selection")
            return

        selected_source = sources[index_choice]

        print(f"\n You selected:\n{selected_source}")

        confirm = input("Type YES/yes to confirm deletion: ").strip()

        if confirm == "YES" or confirm == "yes":
            delete_by_source(selected_source)
            print(" Document deleted successfully")
        else:
            print(" Cancelled")


    # ---------------- STATS ----------------
    elif choice == "3":
        stats = get_index_stats()
        print("\n INDEX STATS:")
        print(stats)


    # ---------------- EXIT ----------------
    elif choice == "4":
        print(" Exiting...")

    else:
        print(" Invalid choice")


if __name__ == "__main__":
    reset_index()