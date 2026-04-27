
""" @app.route('/')
def index():
    filter_date = request.args.get('filter_date')
    todos = Todo.query.all()
    
    if filter_date:
        filter_date = datetime.strptime(filter_date, '%Y-%m-%d').date()
        ongoing_todos = [todo for todo in todos if not todo.completed and todo.deadline.date() == filter_date]
        completed_todos = [todo for todo in todos if todo.deadline and todo.deadline.date() == filter_date]
    else:
        ongoing_todos = sorted((todo for todo in todos if not todo.completed), key=lambda x: x.deadline)
        completed_todos = sorted((todo for todo in todos if todo.completed), key=lambda x: x.deadline or datetime.min)

    completed_count = len(completed_todos)
    total_count = len(ongoing_todos) + len(completed_todos)

    return render_template('index.html', ongoing_todos=ongoing_todos, completed_todos=completed_todos,
                           completed_count=completed_count, total_count=total_count, filter_date=filter_date)




<tbody id="ongoingTodos">
            {% for todo in ongoing_todos %}
            <tr>
                <td>{{ todo.task }}</td>
                <td>{{ todo.date_created.strftime('%Y-%m-%d %H:%M') }}</td>
                <td>{{ todo.deadline.strftime('%Y-%m-%d %H:%M') }}</td>
                <td>Belum Selesai</td>
                <td>
                    <a href="#" onclick="openPopup('{{ todo.note|default('Tidak ada catatan.')|replace("'", "\\'") }}')">Lihat Catatan</a>
                </td>
                
                <td>
                    <a href="/complete/{{ todo.id }}">Complete</a>
                    <a href="/delete/{{ todo.id }}">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody> 
        
        
@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:  # Check if the todo exists
        todo.completed = True
        todo.date_completed = datetime.utcnow()
        db.session.commit()
    return redirect(url_for('index'))
    

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False)
    date_completed = db.Column(db.DateTime)
    note = db.Column(db.String(500))  # Column for notes
    


    <h3>Tugas yang Sudah Selesai</h3>
    <table>
        <thead>
            <tr>
                <th>Tugas</th>
                <th>Tanggal Dibuat</th>
                <th>Deadline</th>
                <th>Status</th>
                <th>Tanggal Selesai</th>
                <th>Catatan</th>
                <th>Aksi</th>
            </tr>
        </thead>
        <tbody id="completedTodos">
            {% for todo in completed_todos %}
            <tr>
                <td>{{ todo.task }}</td>
                <td>{{ todo.date_created.strftime('%Y-%m-%d %H:%M') }}</td>
                <td>{{ todo.deadline.strftime('%Y-%m-%d %H:%M') }}</td>
                <td>Selesai</td>
                <td>{{ todo.date_completed.strftime('%Y-%m-%d %H:%M') }}</td>
                <td>
                    <a href="#" onclick="openPopup('{{ todo.note|default('Tidak ada catatan.')|replace("'", "\\'") }}')">Lihat Catatan</a>
                </td>                
                <td>
                    <a href="/delete/{{ todo.id }}">Delete</a>
                    <a href="/restore/{{ todo.id }}">Kembalikan</a>  <!-- Link to restore the task -->
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>To-Do List</title>
    <link href='https://cdn.jsdelivr.net/npm/fullcalendar@5.10.2/main.css' rel='stylesheet' />
    <script src='https://cdn.jsdelivr.net/npm/fullcalendar@5.10.2/main.js'></script>
    <script src="{{ url_for('static', filename='js/calendar.js') }}"></script>
    <!-- <link rel="stylesheet" href="todo"> -->
<style>
    body {
        background-color: #DFF2EB; /* Warna biru */
        color: #4A628A; /* Warna teks putih untuk kontras yang baik */
        font-family: Arial, sans-serif; /* Font yang bersih dan mudah dibaca */
        margin: 0;
        padding: 20px;
    }
    
    h1 {
        background-color: #7AB2D3; /* Warna latar belakang untuk judul */
        padding: 20px; /* Ruang dalam untuk judul */
        border-radius: 10px; /* Sudut melengkung */
        text-align: center; /* Mengatur judul agar berada di tengah */
        margin-bottom: 20px; /* Jarak bawah */
        color : #DFF2EB
    }
    
    form {
        display: flex;
        flex-direction: column;
        align-items: center; /* Menyelaraskan form ke tengah */
        margin-bottom: 20px;
    }
    
    input[type="text"], input[type="datetime-local"], input[type="date"], textarea {
        width: 80%; /* Lebar input */
        margin: 10px 0;
        padding: 10px; /* Ruang dalam untuk input */
        border: none;
        border-radius: 5px; /* Sudut melengkung */
    }
    
    button {
        background-color: #789DBC; /* Warna latar belakang tombol */
        color: white; /* Warna teks tombol */
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer; /* Menunjukkan bahwa tombol dapat diklik */
    }
    
    button:hover {
        background-color: #0056b3; /* Warna latar belakang tombol saat hover */
        color: white; /* Mengubah warna teks saat hover */
    }
    
    table {
        width: 100%;
        border-collapse: collapse; /* Menghapus jarak antara sel */
        margin-bottom: 20px;
    }
    
    th, td {
        padding: 10px; /* Ruang dalam untuk sel tabel */
        text-align: left; /* Rata kiri untuk teks di tabel */
        border-bottom: 1px solid #ddd; /* Garis bawah untuk sel tabel */
    }
    
    th {
        background-color: #C4E1F6; /* Warna latar belakang untuk header tabel */
    }
    
    .popup {
        display: none; /* Menyembunyikan popup secara default */
        position: fixed; /* Mengatur posisi popup */
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5); /* Latar belakang transparan */
        justify-content: center; /* Menyelaraskan konten popup ke tengah */
        align-items: center; /* Menyelaraskan konten popup ke tengah */
    }
    
    .popup-content {
        background-color: white; /* Latar belakang konten popup */
        padding: 20px;
        border-radius: 10px; /* Sudut melengkung */
        width: 300px; /* Lebar popup */
        text-align: center; /* Rata tengah untuk teks dalam popup */
    }
    
    .close {
        cursor: pointer; /* Menunjukkan bahwa elemen dapat diklik */
    }
    
    
    
</style>
</head>
<body id="todo">
    <h1 id="a1">To-Do List</h1>
    <form id="isi" action="/add" method="POST">
        <input id="a1" type="text" name="task" placeholder="Tugas baru" required>
        <input id="a1" type="datetime-local" name="deadline" required> 
        <textarea id="a1" name="note" rows="3" placeholder="Catatan (opsional)"></textarea>
        <button id="a1" type="submit">Add</button>
    </form>

    <h2 id="a1">Jumlah Tugas: {{ total_count }} | Tugas Selesai: {{ completed_count }}</h2>

    <label for="filterDate">Filter Tanggal Deadline: </label>
    <input type="date" id="filterDate" onchange="filterTasks()">
    

    <h3 id="a1">Tugas yang Belum Selesai</h3>
    <table id="a1">
        <thead id="a1">
            <tr>
                <th>Tugas</th>
                <th>Tanggal Dibuat</th>
                <th>Deadline</th>
                <th>Status</th>
                <th>Catatan</th>
                <th>Aksi</th>
            </tr>
        </thead>

        <tbody id="ongoingTodos">
            {% for todo in ongoing_todos %}
            <tr>
                <td>{{ todo.task }}</td>
                <td>{{ todo.date_created.strftime('%Y-%m-%d %H:%M') }}</td>
                <td>{{ todo.deadline.strftime('%Y-%m-%d %H:%M') }}</td>
                <td>{{ todo.status }}</td> <!-- Display the status -->
                <td>
                    <a href="#" onclick="openPopup('{{ todo.note|default('Tidak ada catatan.')|replace("'", "\\'") }}')">Lihat Catatan</a>
                </td>
                <td>
                    <a href="/complete/{{ todo.id }}">Complete</a>
                    <a href="/delete/{{ todo.id }}">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>

    </table>

    <h3>Tugas yang Sudah Selesai</h3>
    <table>
        <thead>
            <tr>
                <th>Tugas</th>
                <th>Tanggal Dibuat</th>
                <th>Deadline</th>
                <th>Status</th>
                <th>Tanggal Selesai</th>
                <th>Catatan</th>
                <th>Aksi</th>
            </tr>
        </thead>
        <tbody id="completedTodos">
            {% for todo in completed_todos %}
            <tr>
                <td>{{ todo.task }}</td>
                <td>{{ todo.date_created.strftime('%Y-%m-%d %H:%M') }}</td>
                <td>{{ todo.deadline.strftime('%Y-%m-%d %H:%M') }}</td>
                <td>Selesai</td>
                <td>{{ todo.date_completed.strftime('%Y-%m-%d %H:%M') }}</td>
                <td>
                    <a href="#" onclick="openPopup('{{ todo.note|default('Tidak ada catatan.')|replace("'", "\\'") }}')">Lihat Catatan</a>
                </td>                
                <td>
                    <a href="/delete/{{ todo.id }}">Delete</a>
                    <a href="/restore/{{ todo.id }}">Kembalikan</a>  <!-- Link to restore the task -->
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>


    <!-- Popup untuk menampilkan catatan -->
    <div class="popup" id="popup">
        <div class="popup-content">
            <span class="close" onclick="closePopup()">&times;</span>
            <h4>Catatan</h4>
            <p id="popupNoteContent" style="white-space: pre-wrap;"></p>
        </div>
    </div>

    <script>
        function openPopup(note) {
            document.getElementById('popupNoteContent').innerText = note || 'Tidak ada catatan.'; 
            document.getElementById('popup').style.display = 'flex'; 
        }

        function closePopup() {
            document.getElementById('popup').style.display = 'none';
        }

        function filterTasks() {
            const filterDate = document.getElementById("filterDate").value;
            const ongoingTodos = document.getElementById("ongoingTodos").getElementsByTagName("tr");
            const completedTodos = document.getElementById("completedTodos").getElementsByTagName("tr");
        
            // Hide all rows initially
            for (let i = 0; i < ongoingTodos.length; i++) {
                ongoingTodos[i].style.display = "none"; // Hide all ongoing tasks
            }
            for (let i = 0; i < completedTodos.length; i++) {
                completedTodos[i].style.display = "none"; // Hide all completed tasks
            }
        
            // Show only filtered rows based on the selected date
            for (const todo of ongoingTodos) {
                const deadline = todo.cells[2].innerText.split(' ')[0]; // Get only the date part of the deadline
                if (filterDate && deadline === filterDate) {
                    todo.style.display = ""; 
                }
            }
        
            for (const todo of completedTodos) {
                const deadline = todo.cells[2].innerText.split(' ')[0]; // Get only the date part of the deadline
                if (filterDate && deadline === filterDate) {
                    todo.style.display = ""; 
                }
            }
        }
        
    </script>

</body>
</html>






<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Us - SCHEDULO</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #DFF2EB;
            color: #4A628A;
            margin: 0;
            padding: 0;
        }
        header {
            display: flex;
            align-items: center;
            background-color: #b2dcf5;
            padding: 10px;
        }
        nav {
            display: flex;
            align-items: center;
        }
        header img {
            width: 100px;
            padding-left: 70px;
        }
        .links ul {
            list-style-type: none;
            padding: 0;
            display: flex;
        }
        li a {
            color: #493628;
            font-size: 25px;
            font-weight: 700;
            text-decoration: underline;
            border-radius: 25px;
            padding: 15px 20px;
            transition: background-color 0.3s, transform 0.3s;
            margin-left: 100px;
        }
        li a:hover {
            background-color: #608BC1;
            transform: scale(1.05);
        }
        .container {
            padding: 20px;
        }
        .background-info {
            background-color: #B9E5E8; /* Light background for the info box */
            padding: 15px; /* Padding around the text */
            border-radius: 10px; /* Rounded corners */
            margin-bottom: 20px; /* Space below the info box */
        }
        .founders {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .founder {
            perspective: 1000px; /* Perspective for the flip effect */
            margin: 10px; /* Space between cards */
        }
        .founder-card {
            width: 200px; /* Width of the card */
            height: 250px; /* Height of the card */
            position: relative; /* Positioning context for the front and back */
            transition: transform 0.6s; /* Animation duration */
            transform-style: preserve-3d; /* Preserve the 3D effect */
        }
        .founder-card:hover {
            transform: rotateY(180deg); /* Rotate on hover */
        }
        .founder-front, .founder-back {
            position: absolute; /* Positioning for front and back */
            width: 100%;
            height: 100%;
            backface-visibility: hidden; /* Hide back face when not facing */
        }
        .founder-back {
            background-color: #B9E5E8; /* Background color for back */
            transform: rotateY(180deg); /* Rotate back face */
            display:flex; 
            justify-content:center; 
            align-items:center; 
            text-align:center; 
        }
        .founder img {
            border-radius: 50%;
            width: 150px;
            height: 150px;
            object-fit: cover;
        }
    </style>
</head>
<body>

<header>
    <nav>
        <img src="logo.oke.png" alt="Logo SCHEDULO">
        <div class="links">
            <ul>
                <li><a class="active" href="tulis.html">HOME</a></li>
                <li><a href="aboutus.html">ABOUT</a></li>
                <li><a href="http://127.0.0.1:5000">TO DO LIST</a></li>
            </ul>
        </div>
    </nav>
</header>
<div class="container">
    <section>
        <h2>SCHEDULO</h2>

        <div class="background-info">
            <h3> </h3>
            <p>Website ini kami buat atas latar belakang bahwa waktu adalah hal yang berharga dan tidak bisa diulang. Manajemen waktu sangat dibutuhkan untuk menghargai waktu. Oleh karena itu, kami membuat website untuk memudahkan anda dalam membuat to do list. </p>
            <p>Anda bisa menuliskan tugas atau kegiatan yang perlu dilakukan dan menambahkan batas waktu dan juga notes. Selain itu, anda juga bisa menyortir tugas apa saja yang perlu dilakukan pada tanggal yang anda tentukan. </p>
        </div>

       <div class="founders">
           <!-- Founder Card Example -->
           <div class="founder">
                <div class="founder-card" onclick="showMessage('Figilo Pasha Sunni - A passionate developer!')">
                    <div class="founder-front">
                        <img src="fio.jpeg" alt="anggota 1">
                        <h3>Figilo Pasha Sunni</h3>
                    </div>
                    <div class="founder-back">
                        <p>Figilo is known for his innovative ideas in software development.</p>
                    </div>
                </div>
           </div>

           <div class="founder">
                <div class="founder-card" onclick="showMessage('Iqro Septendi - Enthusiastic about AI!')">
                    <div class="founder-front">
                        <img src="iqro.jpeg" alt="anggota 2">
                        <h3>Iqro Septendi</h3>
                    </div>
                    <div class="founder-back">
                        <p>Iqro is an AI enthusiast who loves to explore new technologies.</p>
                    </div>
                </div>
           </div>

           <div class="founder">
                <div class="founder-card" onclick="showMessage('Kalya Andriana - Loves web development!')">
                    <div class="founder-front">
                        <img src="kalya.jpeg" alt="anggota 3">
                        <h3>Kalya Andriana</h3>
                    </div>
                    <div class="founder-back">
                        <p>Kalya specializes in frontend development and user experience.</p>
                    </div>
                </div>
           </div>

           <div class="founder">
                <div class="founder-card" onclick="showMessage('Maria Oktaviani T.K.D - Frontend expert!')">
                    <div class="founder-front">
                        <img src="lala.jpeg" alt="anggota 4">
                        <h3>Maria Oktaviani T.K.D</h3>
                    </div>
                    <div class="founder-back">
                        <p>Maria is a frontend expert with a knack for design.</p>
                    </div>
                </div>
           </div>

           <div class="founder">
                <div class="founder-card" onclick="showMessage('Revaldi Rifwianda - Backend specialist!')">
                    <div class="founder-front">
                        <img src="revaldi.jpeg" alt="anggota 5">
                        <h3>Revaldi Rifwianda</h3>
                    </div>
                    <div class="founder-back">
                        <p>Revaldi excels in backend development and database management.</p>
                    </div>
                </div>
           </div>

       </div>

   </section>
</div>

</body>
</html>


"""
