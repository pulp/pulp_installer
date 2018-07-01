describe directory('/etc/') do
  its('owner') { should eq 'root' }
end

describe file('/var/lib/pulp/database/pulp.sqlite3') do
  it { should exist }
  its('owner') { should eq 'pulp' }
  its('group') { should eq 'pulp' }
  its('size') { should > 300 }
end

['pulp_resource_manager', 'pulp_worker@1', 'pulp_worker@2'].each do |pservice|
  describe service(pservice) do
    it { should be_running }
    it { should be_enabled }
  end
end
