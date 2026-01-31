const { createApp } = Vue;

createApp({
    data() {
        return {
            currentUser: {
                username: '',
                full_name: ''
            },
            users: []
        };
    },

    methods: {
        async loadCurrentUser() {
            try {
                const res = await axios.get('api/hr/me');
                this.currentUser = res.data;
            } catch (err) {
                console.error('خطا در دریافت کاربر جاری', err);
                this.currentUser.full_name = 'کاربر ناشناس';
            }
        },

        async loadUsers() {
            try {
                const res = await axios.get('api/hr/users');
                this.users = res.data;
            } catch (err) {
                console.error('خطا در دریافت لیست کاربران', err);
            }
        }
    },

    mounted() {
        this.loadCurrentUser();
        this.loadUsers();
    }
}).mount('#app');
