describe directory('/etc/') do
  its('owner') { should eq 'root' }
end

describe.one do
  describe directory('/var/lib/pulp/') do
    its('owner') { should eq 'pulp' }
    its('group') { should eq 'pulp' }
  end

  describe directory('/opt/pulp/home/') do
    its('owner') { should eq 'pulp' }
    its('group') { should eq 'pulp' }
  end
end

describe.one do
  describe directory('/var/lib/pulp/tmp') do
    its('owner') { should eq 'pulp' }
    its('group') { should eq 'pulp' }
  end

  describe directory('/opt/pulp/cache/') do
    its('owner') { should eq 'pulp' }
    its('group') { should eq 'pulp' }
  end
end

describe.one do
  describe directory('/var/lib/pulp/assets/') do
    its('owner') { should eq 'pulp' }
    its('group') { should eq 'pulp' }
  end

  describe directory('/opt/pulp/assets/') do
    its('owner') { should eq 'pulp' }
    its('group') { should eq 'pulp' }
  end
end

['pulpcore-api','pulpcore-content', 'pulpcore-worker@1', 'pulpcore-worker@2'].each do |pservice|
  describe service(pservice) do
    it { should be_running }
    it { should be_enabled }
  end
end

describe port(80) do
  it { should be_listening }
end

describe port(443) do
  it { should be_listening }
end

describe http('http://localhost/pulp/api/v3/status/',
               ssl_verify: false) do
    its('status') { should eq 301 }
end

describe http('http://localhost/pulp/api/v3/status/',
               ssl_verify: false, max_redirects: 1) do
    its('status') { should eq 200 }
    its('body') { should match /database_connection/ }
end

describe http('https://localhost/pulp/api/v3/status/',
               ssl_verify: false) do
    its('status') { should eq 200 }
    its('body') { should match /database_connection/ }
end
