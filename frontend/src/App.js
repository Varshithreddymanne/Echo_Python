import { BrowserRouter, Routes, Route } from "react-router-dom";
import Register from "./screens/Register";
import Login from "./screens/Login";
import Feed from "./screens/Feed";
import CreatePost from "./screens/CreatePost";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProtectedRoute><Feed /></ProtectedRoute>} />
        <Route path="/register" element={<ProtectedRoute><Register /></ProtectedRoute>} />
        <Route path="/login" element={<Login />} />
        <Route path="/create" element={<CreatePost />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
