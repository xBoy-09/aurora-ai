

def insert(self, table_name: str, data: dict):
    return (
    self.supabase.table(table_name)
    .insert(data)
    .execute()
    )


def fetch_data(self, table_name: str, query: dict):
    return (
    self.supabase.table(table_name)
    .select("*")
    .eq(**query)
    .execute()
    )


# Upsert data
# response = (
#     supabase.table("instruments")
#     .upsert({"id": 1, "name": "piano"})
#     .execute()
# )



#Update Data
# response = (
#     supabase.table("instruments")
#     .update({"name": "piano"})
#     .eq("id", 1)
#     .execute()
# )


# delete data
# response = (
#     supabase.table("countries")
#     .delete()
#     .eq("id", 1)
#     .execute()
# )