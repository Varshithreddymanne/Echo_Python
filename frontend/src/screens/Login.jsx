import { useState } from "react";
import { VStack, Input, Button, Heading, useToast } from "@chakra-ui/react";
import API from "../api";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const toast = useToast();
  const nav = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await API.post("api/auth/login", form);
      const token = res.data.access_token;
      localStorage.setItem("token", token);
      toast({ title: "Logged in", status: "success" });
      nav("/");
    } catch (err) {
      toast({ title: err?.response?.data?.detail || "Login failed", status: "error" });
    }
  };

  return (
    <VStack spacing={4} p={6}>
      <Heading size="md">Login</Heading>
      <Input placeholder="Email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
      <Input placeholder="Password" type="password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
      <Button onClick={handleLogin}>Login</Button>
    </VStack>
  );
}
