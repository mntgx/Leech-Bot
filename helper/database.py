import motor.motor_asyncio
from config import Config

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.mntgxo_db = self._client[database_name]
        self.col = self.mntgxo_db.user

    def new_user(self, id):
        return dict(
            _id=int(id),                                   
            file_id=None,
            caption=None,
            prefix=None,
            suffix=None,
            metadata=False,
            metadata_code=""" -map 0 -c:s copy -c:a copy -c:v copy -metadata title="Encoded By :- @Madflix_Bots" -metadata author="@JishuDeveloper" -metadata:s:s title="Subtitled By :- @Madflix_Bots" -metadata:s:a title="By :- @Madflix_Bots" -metadata:s:v title="Encoded By :- @Madflix_Bots" """
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)            

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})
    
    # ======================= Thumbnail ======================== #

    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None) if user else None
    
    # ======================= Caption ======================== #

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None) if user else None

    # ======================= Prefix ======================== #

    async def set_prefix(self, id, prefix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'prefix': prefix}})  
        
    async def get_prefix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('prefix', None) if user else None
    
    # ======================= Suffix ======================== #

    async def set_suffix(self, id, suffix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'suffix': suffix}})  
        
    async def get_suffix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('suffix', None) if user else None

    # ======================= Metadata ======================== #
        
    async def set_metadata(self, id, bool_meta):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata': bool_meta}})
        
    async def get_metadata(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata', None) if user else None
        
    # ======================= Metadata Code ======================== #    
        
    async def set_metadata_code(self, id, metadata_code):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata_code': metadata_code}})

    async def get_metadata_code(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata_code', None) if user else None
    
    # ======================= Job Queue ======================== #

    async def add_job(self, bot_id, user_id, message_id, chat_id):
        """Add a job to the queue"""
        try:
            await self.mntgxo_db.jobs.insert_one({
                "bot_id": bot_id,
                "user_id": user_id,
                "message_id": message_id,
                "chat_id": chat_id
            })
            print(f"[DB] Added job: message_id={message_id}, chat_id={chat_id}")
        except Exception as e:
            print(f"[DB ERROR] Failed to add job: {e}")

    async def remove_job(self, bot_id, chat_id, message_id):
        """Remove a job from the queue - fixed parameter order"""
        try:
            result = await self.mntgxo_db.jobs.delete_one({
                "bot_id": bot_id,
                "chat_id": chat_id,
                "message_id": message_id
            })
            if result.deleted_count > 0:
                print(f"[DB] Removed job: message_id={message_id}, chat_id={chat_id}")
            else:
                print(f"[DB WARN] Job not found: message_id={message_id}, chat_id={chat_id}")
        except Exception as e:
            print(f"[DB ERROR] Failed to remove job: {e}")

    async def get_all_jobs(self, bot_id):
        """Get all jobs for a specific bot"""
        try:
            jobs = await self.mntgxo_db.jobs.find({"bot_id": bot_id}).to_list(length=None)
            print(f"[DB] Retrieved {len(jobs)} jobs from database")
            return jobs
        except Exception as e:
            print(f"[DB ERROR] Failed to get jobs: {e}")
            return []
    
    async def clear_all_jobs(self, bot_id):
        """Clear all jobs for a bot (utility function)"""
        try:
            result = await self.mntgxo_db.jobs.delete_many({"bot_id": bot_id})
            print(f"[DB] Cleared {result.deleted_count} jobs")
        except Exception as e:
            print(f"[DB ERROR] Failed to clear jobs: {e}")

mnbots = Database(Config.DB_URL, Config.DB_NAME)
