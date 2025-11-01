import { useState } from "react";
import { VStack, Input, Button, Heading, useToast } from "@chakra-ui/react";
import API from "../api";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const toast = useToast();
  const nav = useNavigate();

  const handleRegister = async () => {
    try {
      await API.post("/auth/register", form);
      toast({ title: "Registered", status: "success" });
      nav("/login");
    } catch (err) {
      toast({ title: err?.response?.data?.detail || "Error", status: "error" });
    }
  };

  return (
    <VStack spacing={4} p={6}>
      <Heading size="md">Register</Heading>
      <Input placeholder="Username" onChange={(e) => setForm({ ...form, username: e.target.value })} />
      <Input placeholder="Email" onChange={(e) => setForm({ ...form, email: e.target.value })} />
      <Input placeholder="Password" type="password" onChange={(e) => setForm({ ...form, password: e.target.value })} />
      <Button onClick={handleRegister}>Register</Button>
    </VStack>
  );
}
