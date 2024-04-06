class UserDataController {

    static getData(req, res) {
        // Fetch users data from your database or any other source
        const users = [
            // Sample user data
            { name: 'John Doe', email: 'john@example.com' },
            { name: 'Jane Smith', email: 'jane@example.com' },
        ];

        res.json({ users });
    }
}

module.exports = UserDataController;