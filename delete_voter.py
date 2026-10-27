import sqlite3

def delete_voter(voter_id):
    conn = sqlite3.connect('secure_vote.db')
    c = conn.cursor()
    
    # Check karein ki voter exist karta hai ya nahi
    c.execute("SELECT * FROM voters WHERE voter_id = ?", (voter_id,))
    voter = c.fetchone()
    
    if voter:
        # Voter ko remove karein
        c.execute("DELETE FROM voters WHERE voter_id = ?", (voter_id,))
        conn.commit()
        print(f"✅ Success: Voter ID '{voter_id}' database se remove ho gaya hai!")
    else:
        print(f"❌ Error: Voter ID '{voter_id}' database mein nahi mila.")
        
    conn.close()

# Jo Voter ID delete karna hai use yahan likhein:
voter_to_remove = "VOTER789"  # Yahan apna target Voter ID dalein
delete_voter(voter_to_remove)