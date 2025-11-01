import { useState, useEffect } from "react";
import { VStack, Input, Textarea, Button, Heading, useToast } from "@chakra-ui/react";
import API from "../api";
import { useNavigate } from "react-router-dom";
import { getUserFromToken } from "../auth";

export default function CreatePost() {
  const [form, setForm] = useState({ title: "", content: "", username: "" });
  const toast = useToast();
  const nav = useNavigate();

  useEffect(() => {
    const user = getUserFromToken();
    if (!user) {
      toast({ title: "Please login first", status: "warning" });
      nav("/login");
      return;
    }
    setForm((prev) => ({ ...prev, username: user.username }));
  }, []);

  const handleCreate = async () => {
    try {
      await API.post("/posts", form);
      toast({ title: "Post created", status: "success" });
      nav("/");
    } catch (err) {
      toast({ title: err?.response?.data?.detail || "Error creating post", status: "error" });
    }
  };

  return (
    <VStack spacing={4} p={6}>
      <Heading size="md">Create Post</Heading>
      <Input
        placeholder="Title"
        value={form.title}
        onChange={(e) => setForm({ ...form, title: e.target.value })}
      />
      <Textarea
        placeholder="Content"
        value={form.content}
        onChange={(e) => setForm({ ...form, content: e.target.value })}
      />
      <Button onClick={handleCreate}>Create</Button>
    </VStack>
  );
}
