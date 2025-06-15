-- RLS Policies for Eviction CRM

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE cases ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE time_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE expenses ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE bills ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE trust_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE collaboration ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;

-- Users table policies
CREATE POLICY "Users can view their own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Users can update their own profile" ON users
    FOR UPDATE USING (auth.uid()::text = id::text);

-- Cases table policies
CREATE POLICY "Users can view their own cases" ON cases
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own cases" ON cases
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own cases" ON cases
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own cases" ON cases
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Contacts table policies
CREATE POLICY "Users can view their own contacts" ON contacts
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own contacts" ON contacts
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own contacts" ON contacts
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own contacts" ON contacts
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Documents table policies
CREATE POLICY "Users can view their own documents" ON documents
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own documents" ON documents
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own documents" ON documents
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own documents" ON documents
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Time entries table policies
CREATE POLICY "Users can view their own time entries" ON time_entries
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own time entries" ON time_entries
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own time entries" ON time_entries
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own time entries" ON time_entries
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Expenses table policies
CREATE POLICY "Users can view their own expenses" ON expenses
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own expenses" ON expenses
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own expenses" ON expenses
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own expenses" ON expenses
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Events table policies
CREATE POLICY "Users can view their own events" ON events
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own events" ON events
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own events" ON events
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own events" ON events
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Bills table policies
CREATE POLICY "Users can view their own bills" ON bills
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own bills" ON bills
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own bills" ON bills
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own bills" ON bills
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Invoices table policies
CREATE POLICY "Users can view their own invoices" ON invoices
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own invoices" ON invoices
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own invoices" ON invoices
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own invoices" ON invoices
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Tasks table policies
CREATE POLICY "Users can view their own tasks" ON tasks
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own tasks" ON tasks
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own tasks" ON tasks
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own tasks" ON tasks
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Trust accounts table policies
CREATE POLICY "Users can view their own trust accounts" ON trust_accounts
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own trust accounts" ON trust_accounts
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own trust accounts" ON trust_accounts
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own trust accounts" ON trust_accounts
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Collaboration table policies
CREATE POLICY "Users can view their own collaboration" ON collaboration
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own collaboration" ON collaboration
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own collaboration" ON collaboration
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own collaboration" ON collaboration
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- Appointments table policies
CREATE POLICY "Users can view their own appointments" ON appointments
    FOR SELECT USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can insert their own appointments" ON appointments
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

CREATE POLICY "Users can update their own appointments" ON appointments
    FOR UPDATE USING (auth.uid()::text = user_id::text);

CREATE POLICY "Users can delete their own appointments" ON appointments
    FOR DELETE USING (auth.uid()::text = user_id::text);

